import logging
from functools import lru_cache
from pathlib import Path

import pygame.display
from pygame import SRCALPHA
from pygame.font import Font

from seagulls.engine import Surface
from seagulls.rendering import (
    Camera,
    Color,
    IPrinter,
    ObjectDoesNotOverlapError,
    Position,
    Size,
    Sprite
)

from ._surface import IProvideSurfaces

logger = logging.getLogger(__name__)


class PygamePrinter(IPrinter):

    _surface: IProvideSurfaces

    def __init__(self, surface: IProvideSurfaces):
        self._surface = surface

    def print_text(
            self,
            text: str,
            font_path: Path,
            font_size: int,
            color: Color,
            size: Size,
            position: Position) -> None:
        try:
            self._assert_visible(size, position)
        except ObjectDoesNotOverlapError:
            return

        c = color.get()
        s = size.get()
        p = self._get_adjusted_position(position).get()

        font = Font(font_path, font_size)
        surface = font.render(text, True, (c["r"], c["g"], c["b"]), "black")
        surface.set_colorkey((0, 0, 0))

        surface = pygame.transform.scale(surface, (s["width"], s["height"]))

        self._get_frame().blit(surface, (p["x"], p["y"]))

    def print_box(self, color: Color, size: Size, border_size: int, position: Position) -> None:
        try:
            self._assert_visible(size, position)
        except ObjectDoesNotOverlapError:
            return

        c = color.get()
        s = size.get()
        p = self._get_adjusted_position(position).get()

        square = Surface((s["width"], s["height"]), SRCALPHA, 32)
        square.fill((c["r"], c["g"], c["b"]))

        center = Surface(
            (s["width"] - border_size * 2, s["height"] - border_size * 2), SRCALPHA, 32)

        square.blit(center, (border_size, border_size))
        square.set_colorkey((0, 0, 0))

        self._get_frame().blit(square, (p["x"], p["y"]))

    def print_square(self, color: Color, size: Size, position: Position) -> None:
        try:
            self._assert_visible(size, position)
        except ObjectDoesNotOverlapError:
            return

        c = color.get()
        s = size.get()
        p = self._get_adjusted_position(position).get()

        square = Surface((s["width"], s["height"]), SRCALPHA, 32)
        square.fill((c["r"], c["g"], c["b"]))
        self._get_frame().blit(square, (p["x"], p["y"]))

    def print_sprite(self, sprite: Sprite, size: Size, position: Position) -> None:
        try:
            self._assert_visible(size, position)
        except ObjectDoesNotOverlapError:
            return

        s = size.get()
        p = self._get_adjusted_position(position).get()

        rez = sprite.resolution().get()
        pos = sprite.position().get()

        sprite_surface = self._load_png(sprite.sprite_grid.file_path)

        unit_surface = Surface((rez["width"], rez["height"]), SRCALPHA, 32)
        unit_surface.blit(
            sprite_surface, (0, 0), (pos["x"], pos["y"], rez["width"], rez["height"]))
        scaled_surface = pygame.transform.scale(unit_surface, (s["width"], s["height"]))
        self._get_frame().blit(scaled_surface, (p["x"], p["y"]))

    def _load_png(self, file: Path) -> Surface:
        loaded_sprite = pygame.image.load(file.resolve())
        if loaded_sprite.get_alpha() is None:
            return loaded_sprite.convert()
        else:
            return loaded_sprite.convert_alpha()

    def commit(self) -> None:
        self._surface.update(self._get_frame())

    def clear(self) -> None:
        self._get_frame.cache_clear()

    def _assert_visible(self, size: Size, position: Position) -> None:
        pass

    def _get_adjusted_position(self, original: Position) -> Position:
        return original

    @lru_cache()
    def _get_frame(self) -> Surface:
        frame = self._surface.get()
        frame.blit(self._get_copy(), (0, 0))
        return frame

    @lru_cache()
    def _get_copy(self) -> Surface:
        return self._surface.get().copy()


class PygameCameraPrinter(PygamePrinter):

    _camera: Camera

    def __init__(self, surface: IProvideSurfaces, camera: Camera):
        super().__init__(surface)
        self._camera = camera

    def _assert_visible(self, size: Size, position: Position) -> None:
        self._camera.assert_visible(size, position)

    def _get_adjusted_position(self, original: Position) -> Position:
        return self._camera.adjust_position(original)


"""
2022-04-12
What if each frame is a new set of objects that we execute, instead of making it a set of objects
we repeatedly call tick() on? We could "tick" future frames before the current one is done
rendering. Access to physics properties of the current frame from future frames can be turned into a
DAG of operations in order to pre-calculate data for a future frame.

```python
class AwaitableReferencePresenter(Protocol):
    def on_ready(self, val: int) -> None: ...

class AwaitableReference:

    # Whether this class is available for interaction
    _available: Event
    _presenter: AwaitableReferencePresenter

    def __init__(self):
        self._available = Event()

    @release_reference
    def execute(self) -> None:
        # Do some stuff
        self._presenter.on_ready(random.randint(1, 100))
```

This is almost certainly a bad idea.
"""
