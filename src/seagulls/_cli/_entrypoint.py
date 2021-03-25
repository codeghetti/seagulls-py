from pathlib import Path

import pygame

from seagulls._asset_manager import AssetManager


class Seagulls:

    _screen: pygame.Surface
    _background: pygame.Surface
    _asset_manager: AssetManager

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self._asset_manager = AssetManager(Path("assets"))
        self._background = self._asset_manager.load_sprite("background", False)

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
        pass

    def _draw(self):
        self.screen.blit(self._background, (0, 0))
        pygame.display.flip()


def main():
    game = Seagulls()
    game.main_loop()
