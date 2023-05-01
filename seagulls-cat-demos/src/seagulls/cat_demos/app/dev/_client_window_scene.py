from seagulls.cat_demos.app.dev._game_server import GameServer, GameServerClient
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEventDispatcher
)
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable


class ClientWindowScene(IExecutable):
    _event_client: GameEventDispatcher
    _server: GameServerClient

    def __init__(
        self,
        event_client: GameEventDispatcher,
        server: GameServerClient,
    ) -> None:
        self._event_client = event_client
        self._server = server

    def __call__(self) -> None:
        self._spawn_server()

    def _spawn_server(self) -> None:
        self._server.execute(GameServer(
            object_id=GameObjectId("server.1"),
            position=Position(x=0, y=0),
            size=Size(width=800, height=800),
        ))
