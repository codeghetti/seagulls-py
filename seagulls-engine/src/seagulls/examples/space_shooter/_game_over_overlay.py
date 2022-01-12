from pathlib import Path

from pygame.font import Font

from seagulls.engine import GameObject, Surface


class GameOverOverlay(GameObject):

    _font: Font

    def __init__(self):
        self._font = Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 50)

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        img = self._font.render(
            "GAME OVER",
            True,
            "red", "black"
        )
        surface.blit(img, (380, 260))
