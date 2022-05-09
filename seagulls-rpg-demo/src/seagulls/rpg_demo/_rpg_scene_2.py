import logging
import random
from functools import lru_cache
from typing import List

from seagulls.pygame import WindowSurface
from seagulls.rendering import (
    IPrinter,
    Position,
)
from ._sprites_client import SpriteSheetLocator, SpriteSheetClient, SpriteClient
from ._rpg_sprites import PixelShmupSpriteSheets, PixelShmupTileSprites, PixelShmupShipSprites
from seagulls.scene import IGameScene, IProvideGameScenes
from seagulls.session import IProvideGameSessions

logger = logging.getLogger(__name__)


class RpgScene2(IGameScene):

    _session: IProvideGameSessions
    _printer: IPrinter
    _tiles_client: SpriteSheetClient

    def __init__(
            self,
            session: IProvideGameSessions,
            printer: IPrinter,
            window: WindowSurface,
            tiles_client: SpriteSheetClient):
        self._session = session
        self._printer = printer
        self._window = window
        self._tiles_client = tiles_client

    def tick(self) -> None:
        mapping = self._tile_mapping()
        for row in range(60):
            for column in range(100):
                x = column * 16
                y = row * 16
                pos = Position({"x": x, "y": y})
                mapping[row][column].render_sprite(pos)

        self._printer.commit()

    @lru_cache()
    def _tile_mapping(self) -> List[List[SpriteClient]]:
        result = []
        for row in range(60):
            row_items = []
            for column in range(100):
                rnd = random.randint(1, 100)
                row_items.append(self._select_sprite(rnd))
            result.append(row_items)

        return result

    def _select_sprite(self, rnd: int) -> SpriteClient:
        options = {
            0: PixelShmupTileSprites.TREE_GRASS_1,
            3: PixelShmupTileSprites.TREE_GRASS_2,
            6: PixelShmupTileSprites.HOME_RED_GRASS_1,
            7: PixelShmupTileSprites.HOME_RED_GRASS_AFRAME,
            8: PixelShmupTileSprites.FLAG_RED_GRASS,
            9: PixelShmupTileSprites.GRASS_1,
            71: PixelShmupTileSprites.GRASS_2,
        }
        matching = 0
        for lower_bound in options.keys():
            if lower_bound < rnd:
                matching = lower_bound

        return self._tiles_client.get_sprite(options[matching])


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
