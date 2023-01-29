import logging

from seagulls.cat_demos.engine.v2._components import (
    MobControlsComponent,
    Position,
    Size,
    SpriteComponent,
)
from seagulls.cat_demos.engine.v2._position_component import PositionComponent
from seagulls.cat_demos.engine.v2._entities import GameComponent, GameObject, GameSprite
from seagulls.cat_demos.engine.v2._resources import ResourceClient
from seagulls.cat_demos.engine.v2._scene import GameSceneObjects
from seagulls.cat_demos.engine.v2._window import GameWindowClient

logger = logging.getLogger(__name__)

window = GameWindowClient()
window.open()
player = GameObject("player")
player_sprite = GameSprite("player.idle")
scene = GameSceneObjects(window)
scene.create_object(player)

positionizer = PositionComponent()
mob_controls = MobControlsComponent(positionizer)
resource_client = ResourceClient()
sprites = SpriteComponent(window, resource_client, positionizer)
sprites.register_sprite(
    sprite=player_sprite,
    resource="/kenney.tiny-dungeon/tilemap-packed.png",
    position=Position(0, 0),
    size=Size(height=50, width=50),
)
sprites.attach_sprite(player, player_sprite)

scene.create_component(GameComponent[PositionComponent]("position"), positionizer)
scene.create_component(GameComponent[MobControlsComponent]("mob-controls"), mob_controls)
scene.create_component(GameComponent[SpriteComponent]("sprites"), sprites)

scene.attach_component(player, GameComponent[MobControlsComponent]("mob-controls"))

for x in range(2000):
    scene.tick()
    logger.error(positionizer.get_position(player))
