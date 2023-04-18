import multiprocessing
from abc import abstractmethod
from functools import lru_cache
from multiprocessing.connection import Connection
from multiprocessing.context import DefaultContext
from typing import NamedTuple, Protocol, Tuple

import pygame
from pygame import SRCALPHA, Surface

from seagulls.cat_demos.app._cli_command import ComponentProviderCollection
from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import GameComponentConfig, GameObjectConfig, GameObjectPrefab, \
    GamePrefabId, \
    IExecutablePrefab
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class GameSubprocessExecutable(Protocol):
    @abstractmethod
    def __call__(self, connection: Connection) -> None:
        pass


class GameServer(NamedTuple):
    object_id: GameObjectId
    position: Position


class GameServerProcess(NamedTuple):
    process_id: int


class DefaultExecutable(GameSubprocessExecutable):

    _app_factory: ServiceProvider[Tuple[SeagullsApp, ServiceProvider[ComponentProviderCollection]]]

    def __init__(
        self,
        app_factory: ServiceProvider[Tuple[SeagullsApp, ServiceProvider[ComponentProviderCollection]]],
    ) -> None:
        self._app_factory = app_factory

    def __call__(self, connection: Connection) -> None:
        app, component_provider = self._app_factory()
        providers = list(component_provider())
        providers.append((GameServerIds.SERVER_PROCESS_CONNECTION, lambda: connection))

        app.run(*providers)


class GameServerPrefab(IExecutablePrefab[GameServer]):

    _scene_objects: SceneObjects
    _object_prefab: GameObjectPrefab
    _window_client: WindowClient
    _executable: GameSubprocessExecutable

    def __init__(
        self,
        scene_objects: SceneObjects,
        object_prefab: GameObjectPrefab,
        window_client: WindowClient,
        executable: GameSubprocessExecutable
    ) -> None:
        self._scene_objects = scene_objects
        self._object_prefab = object_prefab
        self._window_client = window_client
        self._executable = executable

    def __call__(self, config: GameServer) -> None:
        ctx = self._context(config.object_id)
        server_connection, client_connection = self._pipe(config.object_id)
        process = ctx.Process(target=self._executable, args=(server_connection,))
        process.start()

        self._object_prefab(
            GameObjectConfig(
                object_id=config.object_id,
                components=(
                    GameComponentConfig(
                        component_id=GameComponentId[Position]("object-component::position"),
                        config=Position(10, 10),
                    ),
                    GameComponentConfig(
                        component_id=GameComponentId[Size]("object-component::size"),
                        config=Size(
                            width=300,
                            height=300,
                        ),
                    ),
                    GameComponentConfig(
                        component_id=GameComponentId[GameServerProcess]("object-component::server-process"),
                        config=GameServerProcess(
                            process_id=process.pid,
                        ),
                    ),
                )
            ),
        )

    def on_frame_close(self) -> None:
        component_id = GameComponentId[GameServerProcess]("object-component::server-process")
        for object_id in self._scene_objects.find_by_component(component_id):
            position_component = self._scene_objects.get_component(
                object_id,
                GameComponentId[Position]("object-component::position"),
            )
            size_component = self._scene_objects.get_component(
                object_id,
                GameComponentId[Size]("object-component::size"),
            )

            server_screen = Surface(size_component, SRCALPHA, 32)
            server_screen.fill(Color(150, 150, 250))
            _, client_connection = self._pipe(object_id)
            surface = pygame.surfarray.make_surface(client_connection.recv())
            scaled_surface = pygame.transform.scale(surface, size_component - Size(width=4, height=4))
            server_screen.blit(scaled_surface, Position(2, 2))
            self._window_client.get_surface().blit(server_screen, position_component)

    @lru_cache()
    def _pipe(self, object_id: GameObjectId) -> Tuple[Connection, Connection]:
        return self._context(object_id).Pipe()

    @lru_cache()
    def _context(self, object_id: GameObjectId) -> DefaultContext:
        return multiprocessing.get_context("forkserver")


class GameServerIds:
    PREFAB = GamePrefabId[GameServer]("prefab::game-server")
    PREFAB_COMPONENT = GameComponentId[GameServerPrefab]("prefab::game-server")
    SUBPROCESS_EXECUTABLE = GameComponentId[GameSubprocessExecutable]("subprocess-executable")
    SERVER_PROCESS_CONNECTION = GameComponentId[Connection]("server-subprocess-connection")
