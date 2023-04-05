# """
# We have two types of components. Components that are tied to a game object (GameObjectComponent) allow querying against
# the game objects in a scene. Components that are tied to a scene (GameSceneComponent) are not related to game objects
# and provide functionality as part of frame execution. We can think of GameSceneComponents as GameObjectComponents that
# are only tied to a single object in a scene (the scene itself).
#
# For example:
# - a PositionComponent is attached to a game object and provides the ability to get and update the position of the game
#   object in the scene. There is no need to run any code in the scope of the frame.
# - a GunControlsComponent is attached to a game object and spawns a bullet when the firing event is triggered.
# - a UserControlsComponent is attached to a game object but also ticks every frame for each of the game objects.
# - a GameInputComponent has no related game objects and updates once per frame.
# - a SpriteComponent is tied to game objects. Does it tick every frame? Depends on our display implementation.
# - a GameDisplayComponent is tied to the scene and ticks every frame.
#
# New Notes:
# - Activate GameComponents to add functionality to a game.
# - GameComponent register themselves based on their types above.
# - GameComponents can register callbacks to games starting and ending.
# - SceneComponents are attached to scenes and can register callbacks to scenes starting and ending.
# - ObjectComponents are attached to objects and can register callbacks to frames starting and ending.
# """
