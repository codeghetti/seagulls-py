---
title: "seagulls.examples"
---


# [seagulls](../seagulls).examples


??? note "View Source"
    ```python
        from ._main_menu_scene import (
            GenericMenuButton,
            MainMenuScene
        )
        from ._scene_manager import ExampleSceneManager
        from ._session import AsyncGameSession, BlockingGameSession
        from ._simple_stars_background import SimpleStarsBackground
        from ._simple_rpg_background import SimpleRpgBackground
        from ._window_scene import WindowScene
        from ._active_scene_client import (
            IProvideActiveScene,
            ISetActiveScene,
            ActiveSceneClient,
        )

        __all__ = [
            "GenericMenuButton",
            "MainMenuScene",
            "AsyncGameSession",
            "BlockingGameSession",
            "ExampleSceneManager",
            "SimpleStarsBackground",
            "SimpleRpgBackground",
            "WindowScene",
            "IProvideActiveScene",
            "ISetActiveScene",
            "ActiveSceneClient",
        ]

    ```

## GenericMenuButton

```python
class GenericMenuButton(seagulls.engine._game_object.GameObject):
```

Interface for anything representing an object in the scene.

??? note "View Source"
    ```python
        class GenericMenuButton(GameObject):

            _scene: IGameScene
            _offset: int
            _button_text: str

            _asset_manager: AssetManager
            _game_controls: GameControls
            _is_highlighted: Event
            _is_clicked: Event

            _window_height = 768
            _window_width = 1024

            _button_height = 49
            _button_width = 190

            _active_scene_manager: ISetActiveScene

            def __init__(
                    self,
                    scene: IGameScene,
                    offset: int,
                    button_text: str,
                    asset_manager: AssetManager,
                    game_controls: GameControls,
                    active_scene_manager: ISetActiveScene):
                self._scene = scene
                self._offset = offset
                self._button_text = button_text
                self._asset_manager = asset_manager
                self._game_controls = game_controls
                self._active_scene_manager = active_scene_manager

                self._is_highlighted = Event()
                self._is_clicked = Event()

                self._font = Font(Path("assets/fonts/kenvector-future.ttf"), 14)

            def tick(self) -> None:
                self._detect_state()

            def render(self, surface: Surface) -> None:
                button = self._get_background()

                text = self._font.render(self._button_text, True, (90, 90, 70))
                text_height = text.get_height()
                padding = (button.get_height() - text_height) / 2

                button.blit(text, (10, padding))

                surface.blit(button, self._get_position())

            def _detect_state(self) -> None:
                rect = Rect(self._get_position(), (self._button_width, self._button_height))
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self._is_highlighted.set()
                    click = self._game_controls.is_click_initialized()
                    if click:
                        logger.debug("CLICKY")
                        self._is_clicked.set()
                    if not self._game_controls.is_mouse_down():
                        if self._is_clicked.is_set():
                            logger.debug("SWITCH")
                            self._active_scene_manager.set_active_scene(self._scene)
                        self._is_clicked.clear()
                else:
                    self._is_highlighted.clear()
                    self._is_clicked.clear()

            def _get_background(self) -> Surface:
                return self._get_background_map()[self._get_state_name()]

            @lru_cache()
            def _get_background_map(self) -> Dict[str, Surface]:
                return {
                    "normal": self._asset_manager.load_png("ui/blue.button00").copy(),
                    "hover": self._asset_manager.load_png("ui/green.button00").copy(),
                    "click": self._asset_manager.load_png("ui/green.button01").copy(),
                }

            def _get_state_name(self) -> str:
                if self._is_highlighted.is_set():
                    return "click" if self._is_clicked.is_set() else "hover"

                return "normal"

            def _get_position(self) -> Tuple[int, int]:
                left = int((self._window_width / 2) - self._button_width / 2)
                top = int((self._window_height / 2) - self._button_height / 2) + self._offset
                if self._is_clicked.is_set():
                    top += 5

                return left, top

    ```


### GenericMenuButton()

```python
GenericMenuButton(
    scene: seagulls.engine._game_scene.IGameScene,
    offset: int,
    button_text: str,
    asset_manager: seagulls.assets._manager.AssetManager,
    game_controls: seagulls.engine._game_controls.GameControls,
    active_scene_manager: seagulls.examples._active_scene_client.ISetActiveScene
):
```


??? note "View Source"
    ```python
            def __init__(
                    self,
                    scene: IGameScene,
                    offset: int,
                    button_text: str,
                    asset_manager: AssetManager,
                    game_controls: GameControls,
                    active_scene_manager: ISetActiveScene):
                self._scene = scene
                self._offset = offset
                self._button_text = button_text
                self._asset_manager = asset_manager
                self._game_controls = game_controls
                self._active_scene_manager = active_scene_manager

                self._is_highlighted = Event()
                self._is_clicked = Event()

                self._font = Font(Path("assets/fonts/kenvector-future.ttf"), 14)

    ```


### tick()

```python
def tick(self) -> None:
```


??? note "View Source"
    ```python
            def tick(self) -> None:
                self._detect_state()

    ```


### render()

```python
def render(self, surface: pygame.Surface) -> None:
```


??? note "View Source"
    ```python
            def render(self, surface: Surface) -> None:
                button = self._get_background()

                text = self._font.render(self._button_text, True, (90, 90, 70))
                text_height = text.get_height()
                padding = (button.get_height() - text_height) / 2

                button.blit(text, (10, padding))

                surface.blit(button, self._get_position())

    ```


## MainMenuScene

```python
class MainMenuScene(seagulls.engine._game_scene.IGameScene):
```

This class is for X and Y.

??? note "View Source"
    ```python
        class MainMenuScene(IGameScene):

            _surface_renderer: SurfaceRenderer
            _game_controls: GameControls
            _asset_manager: AssetManager

            _game_objects: GameObjectsCollection
            _should_quit: Event

            def __init__(
                    self,
                    surface_renderer: SurfaceRenderer,
                    asset_manager: AssetManager,
                    background: GameObject,
                    game_controls: GameControls,
                    space_shooter_menu_button: GameObject,
                    seagulls_menu_button: GameObject,
                    rpg_menu_button: GameObject):

                self._surface_renderer = surface_renderer
                self._asset_manager = asset_manager
                self._game_controls = game_controls

                self._game_objects = GameObjectsCollection()
                self._game_objects.add(self._game_controls)
                self._game_objects.add(background)
                self._game_objects.add(space_shooter_menu_button)
                self._game_objects.add(seagulls_menu_button)
                self._game_objects.add(rpg_menu_button)

                self._should_quit = Event()

            def start(self) -> None:
                self._surface_renderer.start()
                self.tick()

            def should_quit(self) -> bool:
                return self._should_quit.is_set()

            def tick(self) -> None:
                self._game_objects.apply(lambda x: x.tick())

                if self._game_controls.should_quit():
                    logger.debug("QUIT EVENT DETECTED")
                    self._should_quit.set()

                self._render()

            def _render(self) -> None:
                background = Surface((1024, 600))
                self._game_objects.apply(lambda x: x.render(background))

                self._surface_renderer.render(background)

    ```


### MainMenuScene()

```python
MainMenuScene(
    surface_renderer: seagulls.engine._surface_renderer.SurfaceRenderer,
    asset_manager: seagulls.assets._manager.AssetManager,
    background: seagulls.engine._game_object.GameObject,
    game_controls: seagulls.engine._game_controls.GameControls,
    space_shooter_menu_button: seagulls.engine._game_object.GameObject,
    seagulls_menu_button: seagulls.engine._game_object.GameObject,
    rpg_menu_button: seagulls.engine._game_object.GameObject
):
```


??? note "View Source"
    ```python
            def __init__(
                    self,
                    surface_renderer: SurfaceRenderer,
                    asset_manager: AssetManager,
                    background: GameObject,
                    game_controls: GameControls,
                    space_shooter_menu_button: GameObject,
                    seagulls_menu_button: GameObject,
                    rpg_menu_button: GameObject):

                self._surface_renderer = surface_renderer
                self._asset_manager = asset_manager
                self._game_controls = game_controls

                self._game_objects = GameObjectsCollection()
                self._game_objects.add(self._game_controls)
                self._game_objects.add(background)
                self._game_objects.add(space_shooter_menu_button)
                self._game_objects.add(seagulls_menu_button)
                self._game_objects.add(rpg_menu_button)

                self._should_quit = Event()

    ```


### start()

```python
def start(self) -> None:
```


??? note "View Source"
    ```python
            def start(self) -> None:
                self._surface_renderer.start()
                self.tick()

    ```


### should_quit()

```python
def should_quit(self) -> bool:
```


??? note "View Source"
    ```python
            def should_quit(self) -> bool:
                return self._should_quit.is_set()

    ```


### tick()

```python
def tick(self) -> None:
```


??? note "View Source"
    ```python
            def tick(self) -> None:
                self._game_objects.apply(lambda x: x.tick())

                if self._game_controls.should_quit():
                    logger.debug("QUIT EVENT DETECTED")
                    self._should_quit.set()

                self._render()

    ```


## AsyncGameSession

```python
class AsyncGameSession(seagulls.engine._game_session.IGameSession):
```

Helper class that provides a standard way to create an ABC using
inheritance.

??? note "View Source"
    ```python
        class AsyncGameSession(IGameSession):
            _scene_manager: IProvideGameScenes
            _thread: Thread
            _stopped: Event

            def __init__(self, scene_manager: IProvideGameScenes) -> None:
                self._scene_manager = scene_manager

                self._thread = Thread(target=self._thread_target)
                self._stopped = Event()

            def start(self) -> None:
                logger.debug(f"starting game session")
                self._thread.start()

            def wait_for_completion(self) -> None:
                logger.debug(f"waiting for completion")
                while not self._stopped.is_set():
                    time.sleep(0.1)
                logger.debug(f"done waiting for completion")

            def stop(self) -> None:
                logger.debug(f"stopping game session")
                self._stopped.set()
                self._thread.join()

            def _thread_target(self) -> None:
                pygame.display.set_caption("Our Game")
                scene = self._scene_manager.get_scene()
                scene.start()

                while not self._stopped.is_set() and not scene.should_quit():
                    scene.tick()
                logger.debug("exiting game session")
                self._stopped.set()

    ```


### AsyncGameSession()

```python
AsyncGameSession(
    scene_manager: seagulls.engine._game_scene_manager.IProvideGameScenes
):
```


??? note "View Source"
    ```python
            def __init__(self, scene_manager: IProvideGameScenes) -> None:
                self._scene_manager = scene_manager

                self._thread = Thread(target=self._thread_target)
                self._stopped = Event()

    ```


### start()

```python
def start(self) -> None:
```


??? note "View Source"
    ```python
            def start(self) -> None:
                logger.debug(f"starting game session")
                self._thread.start()

    ```


### wait_for_completion()

```python
def wait_for_completion(self) -> None:
```


??? note "View Source"
    ```python
            def wait_for_completion(self) -> None:
                logger.debug(f"waiting for completion")
                while not self._stopped.is_set():
                    time.sleep(0.1)
                logger.debug(f"done waiting for completion")

    ```


### stop()

```python
def stop(self) -> None:
```


??? note "View Source"
    ```python
            def stop(self) -> None:
                logger.debug(f"stopping game session")
                self._stopped.set()
                self._thread.join()

    ```


## BlockingGameSession

```python
class BlockingGameSession(seagulls.engine._game_session.IGameSession):
```

Helper class that provides a standard way to create an ABC using
inheritance.

??? note "View Source"
    ```python
        class BlockingGameSession(IGameSession):
            _scene_manager: IProvideGameScenes

            def __init__(self, scene_manager: IProvideGameScenes) -> None:
                self._scene_manager = scene_manager

            def start(self) -> None:
                logger.debug(f"starting game session")
                pygame.display.set_caption("Our Game")
                scene = self._scene_manager.get_scene()
                scene.start()

                while not scene.should_quit():
                    scene.tick()
                logger.debug("exiting game session")

            def wait_for_completion(self) -> None:
                pass

            def stop(self) -> None:
                pass

    ```


### BlockingGameSession()

```python
BlockingGameSession(
    scene_manager: seagulls.engine._game_scene_manager.IProvideGameScenes
):
```


??? note "View Source"
    ```python
            def __init__(self, scene_manager: IProvideGameScenes) -> None:
                self._scene_manager = scene_manager

    ```


### start()

```python
def start(self) -> None:
```


??? note "View Source"
    ```python
            def start(self) -> None:
                logger.debug(f"starting game session")
                pygame.display.set_caption("Our Game")
                scene = self._scene_manager.get_scene()
                scene.start()

                while not scene.should_quit():
                    scene.tick()
                logger.debug("exiting game session")

    ```


### wait_for_completion()

```python
def wait_for_completion(self) -> None:
```


??? note "View Source"
    ```python
            def wait_for_completion(self) -> None:
                pass

    ```


### stop()

```python
def stop(self) -> None:
```


??? note "View Source"
    ```python
            def stop(self) -> None:
                pass

    ```


## ExampleSceneManager

```python
class ExampleSceneManager(seagulls.engine._game_scene_manager.IProvideGameScenes):
```

Helper class that provides a standard way to create an ABC using
inheritance.

??? note "View Source"
    ```python
        class ExampleSceneManager(IProvideGameScenes):
            _scene: MainMenuScene

            def __init__(self, scene: MainMenuScene):
                self._scene = scene

            def get_scene(self) -> IGameScene:
                return self._scene

    ```


### ExampleSceneManager()

```python
ExampleSceneManager(scene: seagulls.examples._main_menu_scene.MainMenuScene):
```


??? note "View Source"
    ```python
            def __init__(self, scene: MainMenuScene):
                self._scene = scene

    ```


### get_scene()

```python
def get_scene(self) -> seagulls.engine._game_scene.IGameScene:
```


??? note "View Source"
    ```python
            def get_scene(self) -> IGameScene:
                return self._scene

    ```


## SimpleStarsBackground

```python
class SimpleStarsBackground(seagulls.engine._game_object.GameObject):
```

Interface for anything representing an object in the scene.

??? note "View Source"
    ```python
        class SimpleStarsBackground(GameObject):

            _asset_manager: AssetManager

            def __init__(self, asset_manager: AssetManager):
                self._asset_manager = asset_manager

            def tick(self) -> None:
                pass

            def render(self, surface: Surface) -> None:
                background = self._get_cached_background()
                surface.blit(background, (0, 0))

            @lru_cache()
            def _get_cached_background(self) -> Surface:
                return self._asset_manager.load_sprite("environment/environment-stars").copy()

    ```


### SimpleStarsBackground()

```python
SimpleStarsBackground(asset_manager: seagulls.assets._manager.AssetManager):
```


??? note "View Source"
    ```python
            def __init__(self, asset_manager: AssetManager):
                self._asset_manager = asset_manager

    ```


### tick()

```python
def tick(self) -> None:
```


??? note "View Source"
    ```python
            def tick(self) -> None:
                pass

    ```


### render()

```python
def render(self, surface: pygame.Surface) -> None:
```


??? note "View Source"
    ```python
            def render(self, surface: Surface) -> None:
                background = self._get_cached_background()
                surface.blit(background, (0, 0))

    ```


## SimpleRpgBackground

```python
class SimpleRpgBackground(seagulls.engine._game_object.GameObject):
```

Interface for anything representing an object in the scene.

??? note "View Source"
    ```python
        class SimpleRpgBackground(GameObject):

            _asset_manager: AssetManager
            _game_board: GameBoard

            def __init__(self, asset_manager: AssetManager):
                self._asset_manager = asset_manager
                self._game_board = GameBoard()

            def tick(self) -> None:
                pass

            def render(self, surface: Surface) -> None:
                background = self._get_cached_background()
                surface.blit(background, (0, 0))

            @lru_cache()
            def _get_cached_background(self) -> Surface:
                surface = Surface((1024, 600))

                top_left_corner = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-top-left-corner").copy()
                top_island_edge = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-top-edge").copy()
                top_right_corner = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-top-right-corner").copy()
                island_water = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-water").copy()
                bottom_left_corner = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-bottom-left-corner").copy()
                bottom_island_edge = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-bottom-edge").copy()
                bottom_right_corner = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-bottom-right-corner").copy()
                island_left_edge = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-left-edge").copy()
                island_right_edge = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-right-edge").copy()
                island_grass = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-grass").copy()
                island_red_home = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-red-home").copy()
                island_blue_home = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-blue-home").copy()
                island_tree = self._asset_manager.load_sprite(
                    "environment/rpg-environment/island-tree").copy()

                for y in range(int(600 / 16)):
                    for x in range(int(1024 / 16)):
                        if y == 0:
                            if x == 0:
                                surface.blit(top_left_corner, (x * 16, y * 16))
                            elif x == 63:
                                surface.blit(top_right_corner, (x * 16, y * 16))
                            else:
                                surface.blit(top_island_edge, (x * 16, y * 16))
                        elif y == 35:
                            if x == 0:
                                surface.blit(bottom_left_corner, (x * 16, y * 16))
                            elif x == 63:
                                surface.blit(bottom_right_corner, (x * 16, y * 16))
                            else:
                                surface.blit(bottom_island_edge, (x * 16, y * 16))
                        elif y == 36:
                            surface.blit(island_water, (x * 16, y * 16))

                        elif x == 0:
                            surface.blit(island_left_edge, (x * 16, y * 16))

                        elif x == 63:
                            surface.blit(island_right_edge, (x * 16, y * 16))

                        else:
                            random_number = random.randint(0, 100)
                            if random_number < 92:
                                surface.blit(island_grass, (x * 16, y * 16))
                            elif random_number < 93:
                                if len(self._game_board.get_neighbors(x * 16, y * 16, 16)) == 0:
                                    surface.blit(island_red_home, (x * 16, y * 16))
                                    self._game_board.set_tile(x * 16, y * 16, Tile())
                                else:
                                    surface.blit(island_grass, (x * 16, y * 16))
                            elif random_number < 94:
                                if len(self._game_board.get_neighbors(x * 16, y * 16, 16)) == 0:
                                    surface.blit(island_blue_home, (x * 16, y * 16))
                                    self._game_board.set_tile(x * 16, y * 16, Tile())
                                else:
                                    surface.blit(island_grass, (x * 16, y * 16))
                            else:
                                surface.blit(island_tree, (x * 16, y * 16))
                return surface

    ```


### SimpleRpgBackground()

```python
SimpleRpgBackground(asset_manager: seagulls.assets._manager.AssetManager):
```


??? note "View Source"
    ```python
            def __init__(self, asset_manager: AssetManager):
                self._asset_manager = asset_manager
                self._game_board = GameBoard()

    ```


### tick()

```python
def tick(self) -> None:
```


??? note "View Source"
    ```python
            def tick(self) -> None:
                pass

    ```


### render()

```python
def render(self, surface: pygame.Surface) -> None:
```


??? note "View Source"
    ```python
            def render(self, surface: Surface) -> None:
                background = self._get_cached_background()
                surface.blit(background, (0, 0))

    ```


## WindowScene

```python
class WindowScene(seagulls.engine._game_scene.IGameScene):
```

This class is for X and Y.

??? note "View Source"
    ```python
        class WindowScene(IGameScene):
            _active_scene_provider: IProvideActiveScene
            _should_quit: bool

            def __init__(self, active_scene_provider: IProvideActiveScene):
                self._active_scene_provider = active_scene_provider
                self._should_quit = False

            def start(self) -> None:
                self._active_scene_provider.apply(lambda x: x.start())

            def should_quit(self) -> bool:
                return self._should_quit

            def tick(self) -> None:
                self._active_scene_provider.apply(lambda x: x.tick())
                self._active_scene_provider.apply(self._update_quit_flag)

            def _update_quit_flag(self, scene: IGameScene) -> None:
                self._should_quit = scene.should_quit()

    ```


### WindowScene()

```python
WindowScene(
    active_scene_provider: seagulls.examples._active_scene_client.IProvideActiveScene
):
```


??? note "View Source"
    ```python
            def __init__(self, active_scene_provider: IProvideActiveScene):
                self._active_scene_provider = active_scene_provider
                self._should_quit = False

    ```


### start()

```python
def start(self) -> None:
```


??? note "View Source"
    ```python
            def start(self) -> None:
                self._active_scene_provider.apply(lambda x: x.start())

    ```


### should_quit()

```python
def should_quit(self) -> bool:
```


??? note "View Source"
    ```python
            def should_quit(self) -> bool:
                return self._should_quit

    ```


### tick()

```python
def tick(self) -> None:
```


??? note "View Source"
    ```python
            def tick(self) -> None:
                self._active_scene_provider.apply(lambda x: x.tick())
                self._active_scene_provider.apply(self._update_quit_flag)

    ```


## IProvideActiveScene

```python
class IProvideActiveScene(abc.ABC):
```

Helper class that provides a standard way to create an ABC using
inheritance.

??? note "View Source"
    ```python
        class IProvideActiveScene(ABC):

            @abstractmethod
            def apply(self, callback: Callable[[IGameScene], None]):
                pass

    ```


### apply()

```python
@abstractmethod
def apply(
    self,
    callback: Callable[[seagulls.engine._game_scene.IGameScene], NoneType]
):
```


??? note "View Source"
    ```python
            @abstractmethod
            def apply(self, callback: Callable[[IGameScene], None]):
                pass

    ```


## ISetActiveScene

```python
class ISetActiveScene(abc.ABC):
```

Helper class that provides a standard way to create an ABC using
inheritance.

??? note "View Source"
    ```python
        class ISetActiveScene(ABC):

            @abstractmethod
            def set_active_scene(self, scene: IGameScene) -> None:
                pass

    ```


### set_active_scene()

```python
@abstractmethod
def set_active_scene(self, scene: seagulls.engine._game_scene.IGameScene) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def set_active_scene(self, scene: IGameScene) -> None:
                pass

    ```


## ActiveSceneClient

```python
class ActiveSceneClient(seagulls.examples._active_scene_client.IProvideActiveSceneseagulls.examples._active_scene_client.ISetActiveScene):
```

Helper class that provides a standard way to create an ABC using
inheritance.

??? note "View Source"
    ```python
        class ActiveSceneClient(IProvideActiveScene, ISetActiveScene):

            _active_scene: IGameScene

            def __init__(self, scene: IGameScene):
                self._active_scene = scene

            def apply(self, callback: Callable[[IGameScene], None]):
                callback(self._active_scene)

            def set_active_scene(self, scene: IGameScene) -> None:
                self._active_scene = scene

    ```


### ActiveSceneClient()

```python
ActiveSceneClient(scene: seagulls.engine._game_scene.IGameScene):
```


??? note "View Source"
    ```python
            def __init__(self, scene: IGameScene):
                self._active_scene = scene

    ```


### apply()

```python
def apply(
    self,
    callback: Callable[[seagulls.engine._game_scene.IGameScene], NoneType]
):
```


??? note "View Source"
    ```python
            def apply(self, callback: Callable[[IGameScene], None]):
                callback(self._active_scene)

    ```


### set_active_scene()

```python
def set_active_scene(self, scene: seagulls.engine._game_scene.IGameScene) -> None:
```


??? note "View Source"
    ```python
            def set_active_scene(self, scene: IGameScene) -> None:
                self._active_scene = scene

    ```


