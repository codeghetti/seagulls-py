from argparse import ArgumentParser
from typing import Any, Dict
import logging

import pygame
from seagulls.pygame._game_client import PygameClient
from seagulls.pygame._game_clock import GameTimeUpdater
from seagulls.scenes._simple import SimpleScene

from ._command_interfaces import CliCommand

logger = logging.getLogger(__name__)


class LaunchCommand(CliCommand):

    _pygame_client: PygameClient
    _scene: SimpleScene
    _clock: GameTimeUpdater

    def __init__(
            self,
            pygame_client: PygameClient,
            scene: SimpleScene,
            clock: GameTimeUpdater):
        self._pygame_client = pygame_client
        self._scene = scene
        self._clock = clock

    def get_command_name(self) -> str:
        return "launch"

    def get_command_help(self) -> str:
        return "Launch the seagulls game."

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("--something-else", help="Not any more useful yet")

    def execute(self, args: Dict[str, Any]):
        window = self._pygame_client.open(800, 600)
        self._scene.start()
        window.render_scene(self._scene)

        try:
            should_exit = False
            while not should_exit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        should_exit = True

                self._clock.update()
                self._scene.update()
                window.render_scene(self._scene)
        except KeyboardInterrupt:
            window.close()
