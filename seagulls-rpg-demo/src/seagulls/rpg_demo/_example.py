from seagulls.pygame import WindowSurface, PygamePrinter
from seagulls.rpg_demo._rpg_sprites import PixelShmupSpriteSheets
from seagulls.rpg_demo._sprites_client import SpriteSheetLocator


def _main():
    window = WindowSurface(
        resolution_setting=dict(width=500, height=500),
        camera_setting=dict(width=500, height=500))
    printer = PygamePrinter(surface=window)
    locator = SpriteSheetLocator(printer=printer)
    sheet = locator.get_sprite_sheet(PixelShmupSpriteSheets.SHIPS)
    sprite = sheet.get_sprite()


if __name__ == "__main__":
    _main()
