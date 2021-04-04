from argparse import ArgumentParser
from typing import Any, Dict, Optional
import logging

from seagulls.pygame import (
    GameWindowFactory,
    GameScene, GameControls,
)
from seagulls.pygame import GameTimeUpdater

from ._framework import CliCommand

logger = logging.getLogger(__name__)


class LaunchCommand(CliCommand):

    _window_factory: GameWindowFactory
    _scene: GameScene
    _clock: GameTimeUpdater
    _controls: GameControls

    def __init__(
            self,
            window_factory: GameWindowFactory,
            scene: GameScene,
            clock: GameTimeUpdater,
            controls: GameControls):
        self._window_factory = window_factory
        self._scene = scene
        self._clock = clock
        self._controls = controls

    def get_command_name(self) -> str:
        return "launch"

    def get_command_help(self) -> str:
        return "Launch the seagulls game."

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("--limit-fps", help="Set upper bound FPS limit")

    def execute(self, args: Dict[str, Any]):
        window = self._window_factory.create(800, 600)
        self._scene.start()
        window.render_scene(self._scene)

        try:
            while not self._controls.should_quit():
                self._controls.update()  # Update the game events
                # Our global clock tracks the time between frames
                self._clock.update(self._parse_fps_arg(args.get("limit_fps")))
                self._scene.update()  # The scene tells all the rendered things to update state
                window.render_scene(self._scene)  # Update our window to show the latest scene state
        except KeyboardInterrupt:
            window.close()

    def _parse_fps_arg(self, arg: Optional[int]) -> int:
        return int(arg) if arg else 0
