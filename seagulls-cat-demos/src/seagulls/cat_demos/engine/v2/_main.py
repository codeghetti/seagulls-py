from seagulls.cat_demos.engine.v2._components import PositionComponent
from seagulls.cat_demos.engine.v2._entities import GameComponent, GameObject
from seagulls.cat_demos.engine.v2._scene import GameScene

scene = GameScene()
scene.create_object(GameObject("player"))

positionizer = PositionComponent()

scene.create_component(GameComponent[PositionComponent]("position"), positionizer)
scene.attach_component(GameObject("player"), GameComponent[PositionComponent]("position"))
