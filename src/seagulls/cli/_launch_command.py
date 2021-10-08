from argparse import ArgumentParser
from typing import Any, Dict
import logging

from seagulls.engine import IGameSession

from ._framework import CliCommand

logger = logging.getLogger(__name__)


class LaunchCommand(CliCommand):

    _game_session: IGameSession

    def __init__(self, game_session: IGameSession):
        self._game_session = game_session

    def get_command_name(self) -> str:
        return "launch"

    def get_command_help(self) -> str:
        return "Launch the _seagulls game."

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self, args: Dict[str, Any]):
        try:
            self._game_session.start()
            self._game_session.wait_for_completion()
        except KeyboardInterrupt:
            self._game_session.stop()
