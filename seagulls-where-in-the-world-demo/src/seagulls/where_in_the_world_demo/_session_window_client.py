import pygame
from pygame import Surface


class GameSessionWindowClient:

    def open(self) -> None:
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Where in the World!?")
        pygame.mouse.set_visible(False)
        pygame.font.init()

    def get_surface(self) -> Surface:
        return pygame.display.get_surface()

    def commit(self) -> None:
        pygame.display.flip()

    def close(self) -> None:
        pass
