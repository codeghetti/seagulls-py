import pygame
from pygame import Surface


class WindowClient:

    def open(self) -> None:
        pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Cats!?")
        pygame.mouse.set_visible(False)
        pygame.font.init()

    def get_surface(self) -> Surface:
        return pygame.display.get_surface()

    def commit(self) -> None:
        pygame.display.flip()

    def close(self) -> None:
        pygame.display.quit()
