from seagulls.cat_demos.app.dev._server_prefab import GameServer, GameServerIds
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import PrefabClient
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEventDispatcher
from seagulls.cat_demos.engine.v2.input._pygame import PygameEvents, PygameMouseMotionEvent
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable


class ClientWindowScene(IExecutable):

    _prefab_client: PrefabClient
    _event_client: GameEventDispatcher

    def __init__(
        self,
        prefab_client: PrefabClient,
        event_client: GameEventDispatcher,
    ) -> None:
        self._prefab_client = prefab_client
        self._event_client = event_client

    def __call__(self) -> None:
        self._spawn_server()
        self._spawn_mouse()

    def _spawn_server(self) -> None:
        self._prefab_client.run(GameServerIds.PREFAB, GameServer(
            object_id=GameObjectId("server.1"),
            position=Position(x=0, y=0),
            size=Size(width=400, height=400),
        ))
        self._prefab_client.run(GameServerIds.PREFAB, GameServer(
            object_id=GameObjectId("server.2"),
            position=Position(x=400, y=0),
            size=Size(width=400, height=400),
        ))

    def _spawn_mouse(self) -> None:
        def on_mouse() -> None:
            event = self._event_client.event()
            payload: PygameMouseMotionEvent = event.payload
            print(payload)

        self._event_client.register(PygameEvents.MOUSE_MOTION, on_mouse)

        # self._prefab_client.run(SessionComponents.OBJECT_PREFAB, GameObjectConfig(
        #     object_id=GameObjectId("mouse"),
        #     components=(
        #         GameComponentConfig(
        #             component_id=GameComponentId[Position]("object-component::position"),
        #             config=Position(0, 0),
        #         ),
        #         GameComponentConfig(
        #             component_id=GameComponentId[Sprite]("object-component::sprite"),
        #             config=Sprite(sprite_id=SpriteId("mouse")),
        #         ),
        #     ),
        # ))
        # self._prefab_client.run(MouseControlIds.PREFAB, MouseControls(object_id=GameObjectId("mouse")))
