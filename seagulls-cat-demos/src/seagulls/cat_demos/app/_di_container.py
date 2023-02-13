from typing import Iterable

from functools import lru_cache

from seagulls.seagulls_cli import SeagullsCliApplication

from ._cli_command import GameCliCommand
from ._cli_plugin import CatDemosCliPlugin
from seagulls.cat_demos.engine.v2._input_client import (
    EventPayloadType,
    GameInputClient,
    InputEvent,
    PygameKeyboardInputPublisher,
)
from seagulls.cat_demos.engine.v2._interactors import GameSessionInteractors, IFrame, \
    IProvideFrames, \
    IProvideScenes, IScene
from seagulls.cat_demos.engine.v2._window import GameWindowClient
from seagulls.cat_demos.engine.v2._game_clock import GameClock
from ..engine import GameSession


class StubbyScenes(IProvideScenes):

    def items(self) -> Iterable[IScene]:
        return []


class StubbyFrames(IProvideFrames):

    def items(self) -> Iterable[IFrame]:
        return []


class CatDemosDiContainer:
    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication):
        self._application = application

    @lru_cache()
    def plugin(self) -> CatDemosCliPlugin:
        return CatDemosCliPlugin(
            application=self._application,
            command=self._command(),
        )

    @lru_cache()
    def _command(self) -> GameCliCommand:
        return GameCliCommand(
            game_interactors=self._game_interactors(),
        )

    @lru_cache()
    def _game_session(self) -> GameSession:
        return GameSession(

        )

    @lru_cache()
    def _game_interactors(self) -> GameSessionInteractors:
        return GameSessionInteractors(
            window=GameWindowClient(),
            scenes=StubbyScenes(),
            frames=StubbyFrames(),
            clock=GameClock(),
            input=PygameKeyboardInputPublisher(
                game_input_client=GameInputClient(
                    handlers=tuple([self._on_input_v2])
                ),
            ),
        )

    def _on_input_v2(self, event: InputEvent[EventPayloadType], payload: EventPayloadType) -> None:
        # self._input_v2_routing.route(event, payload)
        # self._event_dispatcher.trigger(event, payload)
        pass
