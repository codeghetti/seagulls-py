import logging
from argparse import ArgumentParser
from typing import Any, Dict

from seagulls.engine import IGameScene, IGameSession
from seagulls.examples import ISetActiveScene

from ._framework import CliCommand

logger = logging.getLogger(__name__)


class LaunchCommand(CliCommand):

    _game_session: IGameSession
    _active_scene_manager: ISetActiveScene

    _main_menu_scene: IGameScene
    _space_shooter_scene: IGameScene
    _seagulls_scene: IGameScene
    _rpg_scene: IGameScene

    def __init__(
            self,
            game_session: IGameSession,
            active_scene_manager: ISetActiveScene,
            main_menu_scene: IGameScene,
            space_shooter_scene: IGameScene,
            seagulls_scene: IGameScene,
            rpg_scene: IGameScene):
        self._game_session = game_session
        self._active_scene_manager = active_scene_manager

        self._main_menu_scene = main_menu_scene
        self._space_shooter_scene = space_shooter_scene
        self._seagulls_scene = seagulls_scene
        self._rpg_scene = rpg_scene

    def get_command_name(self) -> str:
        return "launch"

    def get_command_help(self) -> str:
        return "Launch the _seagulls game."

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--scene",
            choices=["space-shooter", "seagulls", "rpg"],
            help="Load a scene and skip the main menu")

    def execute(self, args: Dict[str, Any]):
        choice = args.get("scene")
        if choice is None:
            choice = "main-menu"

        options = {
            "main-menu": self._main_menu_scene,
            "space-shooter": self._space_shooter_scene,
            "seagulls": self._seagulls_scene,
            "rpg": self._rpg_scene,
        }
        self._active_scene_manager.set_active_scene(options[choice])

        try:
            self._game_session.start()
            self._game_session.wait_for_completion()
        except KeyboardInterrupt:
            self._game_session.stop()
