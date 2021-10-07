from argparse import ArgumentParser
from typing import Any, Dict
import logging

from seagulls.engine import IProvideGameSessions

from ._framework import CliCommand

logger = logging.getLogger(__name__)


class LaunchCommand(CliCommand):

    _game_session_manager: IProvideGameSessions

    def __init__(self, game_session_manager: IProvideGameSessions):
        self._game_session_manager = game_session_manager

    def get_command_name(self) -> str:
        return "launch"

    def get_command_help(self) -> str:
        return "Launch the seagulls game."

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("scene", help="name of scene to load?")

    def execute(self, args: Dict[str, Any]):
        session = self._game_session_manager.get_session(args["scene"])

        try:
            session.start()
            session.wait_for_completion()
        except KeyboardInterrupt:
            session.stop()
