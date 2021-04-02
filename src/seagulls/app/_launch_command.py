from argparse import ArgumentParser
from typing import Any, Dict
import logging

import pygame
from seagulls.pygame._game_client import PygameClient
from seagulls.scenes._simple import SimpleScene

from ._command_interfaces import CliCommand

logger = logging.getLogger(__name__)


class LaunchCommand(CliCommand):

    _pygame_client: PygameClient
    _scene: SimpleScene

    def __init__(
            self,
            pygame_client: PygameClient,
            scene: SimpleScene):
        self._pygame_client = pygame_client
        self._scene = scene

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
                window.render_scene(self._scene)
        except KeyboardInterrupt:
            window.close()

        # scene = GameScene(
        #     background=self._asset_manager.load_sprite("environment/environment-sky"),
        #     objects=[GameObject(
        #         size=pygame.Vector2(64, 64),
        #         position=pygame.Vector2(0, 568),
        #         velocity=pygame.Vector2(1, 0),
        #         sprite=self._asset_manager.load_sprite("wizard/wizard1-stand"),
        #     )],
        # )
        #
        # window.set_title("Seagulls!")
        # window.render_scene(scene)
        #
        # try:
        #     while True:
        #         scene.update()
        #         window.render_scene(scene)
        # except KeyboardInterrupt:
        #     window.close()

        # logger.info("launching the game!")
        # pygame.init()
        # pygame.display.set_caption("Seagulls")
        #
        # self._screen = pygame.display.set_mode((800, 600))
        # self._asset_manager = AssetManager(Path("assets"))
        # self._background = self._asset_manager.load_sprite("background", False)
        # self._clock = pygame.time.Clock()
        #
        # self._player = GameObject(
        #     pygame.Vector2(400, 300),
        #     self._asset_manager.load_sprite("seagull/seagull-got-hit"),
        #     pygame.Vector2(0, 0),
        # )
        # self._poop = GameObject(
        #     pygame.Vector2(400, 400),
        #     self._asset_manager.load_sprite("poop/poop-falling"),
        #     pygame.Vector2(0, 1),
        # )
        #
        # self.main_loop()

    # def main_loop(self):
    #     while True:
    #         self._handle_input()
    #         self._process_game_logic()
    #         self._draw()
    #
    # def _handle_input(self):
    #     for event in pygame.event.get():
    #         if self._should_quit(event):
    #             quit()
    #
    # def _should_quit(self, event):
    #     if event.type == pygame.QUIT:
    #         return True
    #     if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
    #         return True
    #
    #     return False
    #
    # def _process_game_logic(self):
    #     self._player.move()
    #     self._poop.move()
    #
    # def _draw(self):
    #     self._screen.blit(self._background, (0, 0))
    #     self._player.draw(self._screen)
    #     self._poop.draw(self._screen)
    #     pygame.display.flip()
    #     self._clock.tick(60)
