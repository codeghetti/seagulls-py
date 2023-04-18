from seagulls.cat_demos.app.dev._server_prefab import GameServer, GameServerIds
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import PrefabClient
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEventDispatcher
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

    def _spawn_server(self) -> None:
        print("running spawn server prefab")
        self._prefab_client.run(GameServerIds.PREFAB, GameServer(
            object_id=GameObjectId("server"),
            position=Position(x=0, y=0),
        ))
