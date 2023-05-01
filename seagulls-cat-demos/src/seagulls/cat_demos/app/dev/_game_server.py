import logging
import multiprocessing
import pygame
import uuid
from abc import abstractmethod
from datetime import datetime
from multiprocessing.connection import Connection
from multiprocessing.context import DefaultContext, Process
from pygame import SRCALPHA, Surface
from threading import Event
from typing import (
    Any,
    Callable,
    Dict,
    NamedTuple,
    Protocol,
    Tuple,
    TypeAlias,
    cast
)
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from seagulls.cat_demos.app._cli_command import ComponentProviderCollection
from seagulls.cat_demos.engine.v2.components._client_containers import GameClientProvider
from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._entities import GameClientId, GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent,
    GameEventDispatcher
)
from seagulls.cat_demos.engine.v2.input._pygame import (
    PygameEvents,
    PygameKeyboardEvent,
    PygameMouseMotionEvent
)
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp
from seagulls.cat_demos.engine.v2.window._window import (
    SurfaceBytes,
    WindowClient
)

logger = logging.getLogger(__name__)


class GameSubprocessExecutable(Protocol):
    @abstractmethod
    def __call__(self, connection: Connection) -> None:
        pass


class GameServer(NamedTuple):
    object_id: GameObjectId
    position: Position
    size: Size


class GameServerProcess(NamedTuple):
    process_id: int
    forward_input: bool


class DateTime(NamedTuple):
    value: datetime


class DefaultExecutable(GameSubprocessExecutable):
    _app_factory: GameClientProvider[
        Tuple[SeagullsApp, GameClientProvider[ComponentProviderCollection]]
    ]

    def __init__(
        self,
        app_factory: GameClientProvider[
            Tuple[SeagullsApp, GameClientProvider[ComponentProviderCollection]]
        ],
    ) -> None:
        self._app_factory = app_factory

    def __call__(self, connection: Connection) -> None:
        app, component_provider = self._app_factory()
        providers = list(component_provider())
        providers.append((GameServerComponent.SERVER_PROCESS_CONNECTION, lambda: connection))

        try:
            app.run(*providers)
        except KeyboardInterrupt:
            pass


class ServerEventForwarder:
    _connection: Connection  # The server uses this end of the pipe to send and recv data
    _event_client: GameEventDispatcher

    def __init__(
        self, connection: Connection, event_client: GameEventDispatcher
    ) -> None:
        self._connection = connection
        self._event_client = event_client

    def tick(self) -> None:
        # TODO: this feels risky if the other side of the pipe doesn't stop sending events
        # we could use a special event to stop this loop
        # kinda like a commit event?
        while self._connection.poll():
            event = self._connection.recv()
            self._event_client.trigger(GameEvent(*event))


class ClientConnection(Connection):
    """
    Type used as a way to announce you specifically want to write client code.
    """


class ServerConnection(Connection):
    """
    Type used as a way to announce you specifically want to write server code.
    """


Pid: TypeAlias = int
_ProcessDict: TypeAlias = Dict[
    Pid, Tuple[DefaultContext, Process, ClientConnection, ServerConnection]
]


class GameServerProcessManager:
    _processes: _ProcessDict

    def __init__(self) -> None:
        self._processes = {}

    def start(self, target: Callable[[Any], Any]) -> Pid:
        # TODO: figure out how to support windows
        context = multiprocessing.get_context("forkserver")
        client_connection, server_connection = context.Pipe()
        process = context.Process(target=target, args=(server_connection,))
        process.start()
        if not process.pid:
            raise RuntimeError("Not sure why process hasn't started yet.")

        self._processes[process.pid] = (
            cast(DefaultContext, context),
            cast(Process, process),
            cast(ClientConnection, client_connection),
            cast(ServerConnection, server_connection),
        )

        return process.pid

    def get_client_connection(self, pid: int) -> ClientConnection:
        return self._processes[pid][2]

    def get_server_connection(self, pid: int) -> ServerConnection:
        return self._processes[pid][3]


class FilesystemMonitor(FileSystemEventHandler):
    _trigger: Event

    def __init__(self) -> None:
        self._trigger = Event()

    def on_modified(self, event) -> None:
        self._trigger.set()

    def toggled(self) -> bool:
        return self._trigger.is_set()

    def reset(self) -> None:
        self._trigger.clear()


class GameServerClient:
    _scene_objects: SceneObjects
    _window_client: WindowClient
    _event_client: GameEventDispatcher
    _executable: GameSubprocessExecutable
    _process_manager: GameServerProcessManager
    _filesystem_monitor: FilesystemMonitor

    def __init__(
        self,
        scene_objects: SceneObjects,
        window_client: WindowClient,
        event_client: GameEventDispatcher,
        executable: GameSubprocessExecutable,
        process_manager: GameServerProcessManager,
        filesystem_monitor: FilesystemMonitor,
    ) -> None:
        self._scene_objects = scene_objects
        self._window_client = window_client
        self._event_client = event_client
        self._executable = executable
        self._process_manager = process_manager
        self._filesystem_monitor = filesystem_monitor

    def execute(self, request: GameServer) -> None:
        # TODO: I would like to be able to describe this scenario:
        #       "while this process is running, listen to events to communicate with the server"
        #       client.while(condition, game_object_context)
        pid = self._process_manager.start(self._executable)
        logger.debug(f"started game server: {pid}")

        self._scene_objects.add(request.object_id)
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[Position]("position"),
            config=request.position,
        )
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[Size]("size"),
            config=request.size,
        )
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[GameServerProcess]("server-process"),
            config=GameServerProcess(process_id=pid, forward_input=True),
        )
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[DateTime]("created-at"),
            config=DateTime(datetime.now()),
        )

    def on_scene_open(self) -> None:
        component_id = ObjectDataId[GameServerProcess](
            "object-component::server-process"
        )

        def _on_mouse_motion() -> None:
            for object_id in self._scene_objects.find_by_data_id(component_id):
                self._send_mouse_event(object_id)

        def _on_keyboard() -> None:
            for object_id in self._scene_objects.find_by_data_id(component_id):
                # print(f"forwarding event to object: {object_id}")
                self._send_keyboard_event(object_id)

        self._event_client.register(PygameEvents.MOUSE_MOTION, _on_mouse_motion)
        self._event_client.register(PygameEvents.KEYBOARD, _on_keyboard)

        observer = Observer()
        handler = self._filesystem_monitor
        observer.schedule(handler, "src/", recursive=True)
        observer.start()

    def on_frame_close(self) -> None:
        component_id = ObjectDataId[GameServerProcess](
            "object-component::server-process"
        )

        toggled = self._filesystem_monitor.toggled()
        if toggled:
            self._filesystem_monitor.reset()

        # TODO: make a version that returns a tuple[objectid, component]
        for object_id in self._scene_objects.find_by_data_id(component_id):
            process_component = self._scene_objects.get_data(
                object_id, component_id
            )

            client_connection = self._process_manager.get_client_connection(
                process_component.process_id
            )
            position_component = self._scene_objects.get_data(
                object_id,
                ObjectDataId[Position]("object-component::position"),
            )
            size_component = self._scene_objects.get_data(
                object_id,
                ObjectDataId[Size]("object-component::size"),
            )

            if toggled:
                client_connection.send(GameEvent(PygameEvents.QUIT, None))
                self._scene_objects.remove(object_id)
                self.execute(
                    GameServer(
                        object_id=GameObjectId(str(uuid.uuid4())),
                        position=position_component,
                        size=size_component,
                    )
                )

            if client_connection.poll():
                event: SurfaceBytes = client_connection.recv().payload

                server_screen = Surface(size_component, SRCALPHA, 32)
                server_screen.fill(Color(10, 10, 10))
                surface = pygame.image.frombytes(event.bytes, event.size, "RGBA")
                scaled_surface = pygame.transform.scale(
                    surface, size_component - Size(width=4, height=4)
                )
                server_screen.blit(scaled_surface, Position(2, 2))
                self._window_client.get_surface().blit(
                    server_screen, position_component
                )

    def _send_mouse_event(self, object_id: GameObjectId) -> None:
        component_id = ObjectDataId[GameServerProcess](
            "object-component::server-process"
        )
        process_component = self._scene_objects.get_data(object_id, component_id)

        client_connection = self._process_manager.get_client_connection(
            process_component.process_id
        )

        event = self._event_client.event()
        payload: PygameMouseMotionEvent = event.payload
        client_connection.send((event.id, payload))

    def _send_keyboard_event(self, object_id: GameObjectId) -> None:
        component_id = ObjectDataId[GameServerProcess](
            "object-component::server-process"
        )
        process_component = self._scene_objects.get_data(object_id, component_id)

        # TODO: this shouldn't be necessary here
        event = self._event_client.event()
        payload: PygameKeyboardEvent = event.payload

        client_connection = self._process_manager.get_client_connection(
            process_component.process_id
        )

        if payload.type in [pygame.KEYDOWN, pygame.KEYUP]:
            client_connection.send(
                (
                    PygameEvents.KEYBOARD,
                    PygameKeyboardEvent(type=payload.type, key=payload.key),
                )
            )
            client_connection.send(
                (
                    PygameEvents.key(payload.key),
                    PygameKeyboardEvent(type=payload.type, key=payload.key),
                )
            )
        if payload.type == pygame.KEYDOWN:
            client_connection.send(
                (
                    PygameEvents.key_pressed(payload.key),
                    PygameKeyboardEvent(type=payload.type, key=payload.key),
                )
            )
        if payload.type == pygame.KEYUP:
            client_connection.send(
                (
                    PygameEvents.key_released(payload.key),
                    PygameKeyboardEvent(type=payload.type, key=payload.key),
                )
            )

        client_connection.send((event.id, payload))


class GameServerComponent:
    CLIENT_ID = GameClientId[GameServerClient]("game-server-client")
    SUBPROCESS_EXECUTABLE = GameClientId[GameSubprocessExecutable]("subprocess-executable")
    SERVER_PROCESS_CONNECTION = GameClientId[Connection]("server-subprocess-connection")
    SERVER_MSG_HANDLER = GameClientId[ServerEventForwarder]("server-message-handler")
