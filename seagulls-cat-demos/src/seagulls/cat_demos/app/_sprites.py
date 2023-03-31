from seagulls.cat_demos.engine.v2._sprite_component import GameSprite, IManageSprites
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.position._position_component import Position


class MySprites:
    PLAYER_IDLE_1 = GameSprite("player.idle.1")
    PLAYER_IDLE_2 = GameSprite("player.idle.2")
    ENEMY_IDLE = GameSprite("enemy.idle")


class GameSpritesPlugin:

    def __init__(self) -> None:
        pass

    def register_sprites(self, client: IManageSprites) -> None:
        client.register_sprite(
            sprite=MySprites.PLAYER_IDLE_1,
            resource="/kenney.tiny-dungeon/tilemap-packed.png",
            position=Position(x=16, y=16 * 7),
            size=Size(height=16, width=16),
        )
        client.register_sprite(
            sprite=MySprites.PLAYER_IDLE_2,
            resource="/kenney.tiny-dungeon/tilemap-packed.png",
            position=Position(x=16 * 2, y=16 * 7),
            size=Size(height=16, width=16),
        )
        client.register_sprite(
            sprite=MySprites.ENEMY_IDLE,
            resource="/kenney.tiny-dungeon/tilemap-packed.png",
            position=Position(x=16, y=16 * 9),
            size=Size(height=16, width=16),
        )
