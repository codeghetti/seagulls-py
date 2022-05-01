import logging
from functools import lru_cache
from pathlib import Path

import pygame.display

from seagulls.engine import Surface
from seagulls.rendering import Color, IPrinter, Position, Size

from ._surface import IProvideSurfaces
from ..rendering._sprite import Sprite

logger = logging.getLogger(__name__)


class PygamePrinter(IPrinter):

    _surface: IProvideSurfaces

    def __init__(self, surface: IProvideSurfaces):
        self._surface = surface

    def print_square(self, color: Color, size: Size, position: Position):
        c = color.get()
        s = size.get()
        p = position.get()

        square = Surface((s["width"], s["height"]))
        square.fill((c["r"], c["g"], c["b"]))
        self._get_frame().blit(square, (p["x"], p["y"]))

    def print_sprite(self, sprite: Sprite, size: Size, position: Position) -> None:
        s = size.get()
        p = position.get()

        rez = sprite.resolution().get()
        pos = sprite.position().get()

        sprite_surface = self._load_png(sprite.sprite_grid.file_path)

        unit_surface = Surface((rez["width"], rez["height"]))
        unit_surface.set_colorkey((0, 0, 0))
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

    @lru_cache()
    def _get_frame(self) -> Surface:
        frame = self._surface.get()
        frame.blit(self._get_copy(), (0, 0))
        return frame

    @lru_cache()
    def _get_copy(self) -> Surface:
        return self._surface.get().copy()


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
