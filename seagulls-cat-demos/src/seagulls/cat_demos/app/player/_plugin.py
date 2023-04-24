from seagulls.cat_demos.engine.v2.collisions._collider_component import ColliderPrefabIds
from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentContainer
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp, SessionComponents
from ._player_controls import PlayerControlsPrefab


class PlayerPlugin:

    _scene_components: GameComponentContainer

    def __init__(self, scene_components: GameComponentContainer) -> None:
        self._scene_components = scene_components

    def player_controls_prefab(self):
        return PlayerControlsPrefab(
            scene_objects=self._scene_components.get(SessionComponents.SCENE_OBJECTS),
            event_client=self._scene_components.get(SessionComponents.EVENT_CLIENT),
            toggles=self._scene_components.get(SessionComponents.INPUT_TOGGLES_CLIENT),
            clock=self._scene_components.get(SessionComponents.SCENE_CLOCK),
            collisions=self._scene_components.get(ColliderPrefabIds.PREFAB_COMPONENT),
        )


def entry_point(app: SeagullsApp) -> None:
    # app.add_plugin(PlayerPlugin(app.scene_components()))
    pass
