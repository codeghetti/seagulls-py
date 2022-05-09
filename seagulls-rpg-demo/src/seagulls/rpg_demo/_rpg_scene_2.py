import logging

from seagulls.pygame import WindowSurface
from seagulls.rendering import (
    IPrinter,
    Position,
)
from ._sprites_client import SpriteSheetLocator
from ._rpg_sprites import PixelShmupSpriteSheets, PixelShmupTileSprites, PixelShmupShipSprites
from seagulls.scene import IGameScene, IProvideGameScenes
from seagulls.session import IProvideGameSessions

logger = logging.getLogger(__name__)


class RpgScene2(IGameScene):

    _session: IProvideGameSessions
    _printer: IPrinter

    def __init__(
            self,
            session: IProvideGameSessions,
            printer: IPrinter,
            window: WindowSurface):
        self._session = session
        self._printer = printer
        self._window = window
        pass

    def tick(self) -> None:
        sprite_sheet_locator = SpriteSheetLocator(printer=self._printer)

        tiles = sprite_sheet_locator.get_sprite_sheet(
            sprite_sheet_id=PixelShmupSpriteSheets.TILES
        )
        ships = sprite_sheet_locator.get_sprite_sheet(
            sprite_sheet_id=PixelShmupSpriteSheets.SHIPS
        )

        large_blue = ships.get_sprite(PixelShmupShipSprites.MODEL_1_LARGE_BLUE)

        grass_tree_1 = tiles.get_sprite(PixelShmupTileSprites.TREE_GRASS_1)
        grass_tree_2 = tiles.get_sprite(PixelShmupTileSprites.TREE_GRASS_2)

        grass_tree_1.render_sprite(Position({"x": 100, "y": 100}))
        grass_tree_1.render_sprite(Position({"x": 200, "y": 100}), scale=2.0)
        grass_tree_1.render_sprite(Position({"x": 300, "y": 100}))

        grass_tree_2.render_sprite(Position({"x": 300, "y": 300}), scale=3.0)

        large_blue.render_sprite(Position({"x": 300, "y": 500}))

        self._printer.commit()


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
