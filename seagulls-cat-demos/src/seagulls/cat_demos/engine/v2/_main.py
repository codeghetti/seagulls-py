import logging

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._game_objects import GameObjectId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._client import GameEventDispatcher
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp, SessionComponents
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.text._component import Text
from seagulls.cat_demos.engine.v2.window._window import WindowClient

logger = logging.getLogger(__name__)


class OpenScene(IExecutable):
    _scene_objects: SceneObjects
    _scene_event_client: GameEventDispatcher
    _window_client: WindowClient

    def __init__(
            self,
            scene_objects: SceneObjects,
            scene_event_client: GameEventDispatcher,
            window_client: WindowClient,
    ) -> None:
        self._scene_objects = scene_objects
        self._scene_event_client = scene_event_client
        self._window_client = window_client

    def __call__(self) -> None:
        logger.debug("index scene open")
        self._scene_objects.add(GameObjectId("hello-world"))

        self._add_position()
        self._add_text()

    def _add_position(self):
        self._scene_objects.attach_component(
            GameObjectId("hello-world"),
            GameComponentId[Position]("position.object-component"),
        )
        component = self._scene_objects.open_component(
            GameObjectId("hello-world"),
            GameComponentId[Position]("position.object-component"),
        )
        component.set(Position(x=5, y=20))

    def _add_text(self):
        self._scene_objects.attach_component(
            GameObjectId("hello-world"),
            GameComponentId[Text]("text.object-component"),
        )
        component = self._scene_objects.open_component(
            GameObjectId("hello-world"),
            GameComponentId[Text]("text.object-component"),
        )
        component.set(Text("Hello, Hello, Hello!"))


app = SeagullsApp()

component_factory = app.component_factory()
session_components = app.session_components()
scene_components = app.scene_components()

app.run(
    (SessionComponents.INDEX_OPEN_EXECUTABLE, lambda: OpenScene(
        scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
        scene_event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
        window_client=session_components.get(SessionComponents.WINDOW_CLIENT),
    ))
)
