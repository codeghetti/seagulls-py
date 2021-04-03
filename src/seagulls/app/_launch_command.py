from argparse import ArgumentParser
from typing import Any, Dict
import logging

import pygame
from seagulls.pygame import GameWindowFactory
from seagulls.pygame import GameTimeUpdater
from seagulls.scenes import SimpleScene

from ._command_interfaces import CliCommand

logger = logging.getLogger(__name__)


class LaunchCommand(CliCommand):

    _window_factory: GameWindowFactory
    _scene: SimpleScene
    _clock: GameTimeUpdater

    def __init__(
            self,
            window_factory: GameWindowFactory,
            scene: SimpleScene,
            clock: GameTimeUpdater):
        self._window_factory = window_factory
        self._scene = scene
        self._clock = clock

    def get_command_name(self) -> str:
        return "launch"

    def get_command_help(self) -> str:
        return "Launch the seagulls game."

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("--something-else", help="Not any more useful yet")

    def execute(self, args: Dict[str, Any]):
        window = self._window_factory.create(800, 600)
        self._scene.start()
        window.render_scene(self._scene)

        try:
            should_exit = False
            while not should_exit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        should_exit = True

                self._clock.update()  # Our global clock tracks the time between frames
                self._scene.update()  # The scene tells all the rendered things to update state
                window.render_scene(self._scene)  # Update our window to show the latest scene state
        except KeyboardInterrupt:
            window.close()
