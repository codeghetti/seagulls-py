from pathlib import Path

import pygame

from seagulls._asset_manager import AssetManager
from seagulls._game_object import GameObject


class Seagulls:

    _screen: pygame.Surface
    _background: pygame.Surface
    _asset_manager: AssetManager

    def __init__(self):
        self._init_pygame()
        self._screen = pygame.display.set_mode((800, 600))
        self._asset_manager = AssetManager(Path("assets"))
        self._background = self._asset_manager.load_sprite("background", False)

        self._player = GameObject(
            pygame.Vector2(400, 300),
            self._asset_manager.load_sprite("seagull/seagull-got-hit"),
            pygame.Vector2(0, 0),
        )
        self._poop = GameObject(
            pygame.Vector2(400, 400),
            self._asset_manager.load_sprite("poop/poop-falling"),
            pygame.Vector2(0, 0.2),
        )

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Seagulls")

    def _handle_input(self):
        for event in pygame.event.get():
            if self._should_quit(event):
                quit()

    def _should_quit(self, event):
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True

        return False

    def _process_game_logic(self):
        self._player.move()
        self._poop.move()

    def _draw(self):
        self._screen.blit(self._background, (0, 0))
        self._player.draw(self._screen)
        self._poop.draw(self._screen)
        pygame.display.flip()


def main():
    game = Seagulls()
    game.main_loop()
