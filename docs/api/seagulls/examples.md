---
title: "seagulls.examples"
---


# [seagulls](../seagulls).examples


??? note "View Source"
    ```python
        from ._main_menu_scene import MainMenuScene
        from ._scene_manager import ExampleSceneManager
        from ._session import AsyncGameSession, BlockingGameSession
        from ._simple_stars_background import SimpleStarsBackground
        from ._simple_rpg_background import SimpleRpgBackground
        from ._window_scene import WindowScene
        from ._game_state import GameState

        __all__ = [
            "MainMenuScene",
            "AsyncGameSession",
            "BlockingGameSession",
            "ExampleSceneManager",
            "SimpleStarsBackground",
            "SimpleRpgBackground",
            "WindowScene",
            "GameState"
        ]

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
            _space_shooter_menu_button: SpaceShooterMenuButton
            _seagulls_menu_button: SeagullsMenuButton
            _rpg_menu_button: RpgMenuButton
            _should_quit: Event

            _game_state: GameState
            _space_shooter_scene: IGameScene
            _seagulls_scene: IGameScene
            _rpg_scene: IGameScene

            def __init__(
                    self,
                    surface_renderer: SurfaceRenderer,
                    asset_manager: AssetManager,
                    background: GameObject,
                    game_controls: GameControls,
                    game_state: GameState,
                    space_shooter_scene: IGameScene,
                    seagulls_scene: IGameScene,
                    rpg_scene: IGameScene,):

                self._surface_renderer = surface_renderer
                self._asset_manager = asset_manager
                self._game_controls = game_controls
                self._game_state = game_state

                self._space_shooter_scene = space_shooter_scene
                self._seagulls_scene = seagulls_scene
                self._rpg_scene = rpg_scene

                self._game_objects = GameObjectsCollection()
                self._game_objects.add(background)
                self._space_shooter_menu_button = SpaceShooterMenuButton(
                    asset_manager=asset_manager,
                    game_controls=game_controls,
                )
                self._seagulls_menu_button = SeagullsMenuButton(
                    asset_manager=asset_manager,
                    game_controls=game_controls,
                )
                self._rpg_menu_button = RpgMenuButton(
                    asset_manager=asset_manager,
                    game_controls=game_controls,
                )

                self._game_objects.add(self._space_shooter_menu_button)
                self._game_objects.add(self._seagulls_menu_button)
                self._game_objects.add(self._rpg_menu_button)
                self._game_objects.add(self._game_controls)

                self._should_quit = Event()

            def start(self) -> None:
                self._surface_renderer.start()
                self.tick()

            def should_quit(self) -> bool:
                return self._should_quit.is_set()

            def tick(self) -> None:
                self._game_objects.apply(lambda x: x.tick())
                if self._space_shooter_menu_button.should_switch:
                    logger.debug("SWITCHING SCENE TO SPACE SHOOTER")
                    self._change_scene(self._space_shooter_scene)
                if self._seagulls_menu_button.should_switch:
                    logger.debug("SWITCHING SCENE TO SEAGULLS")
                    self._change_scene(self._seagulls_scene)
                if self._rpg_menu_button.should_switch:
                    logger.debug("SWITCHING SCENE TO RPG")
                    self._change_scene(self._rpg_scene)
                if self._game_controls.should_quit():
                    logger.debug("QUIT EVENT DETECTED")
                    self._should_quit.set()

                self._render()

            def _change_scene(self, next_scene: IGameScene) -> None:
                self._game_state.active_scene = next_scene
                self._game_state.game_state_changed = True

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
    game_state: seagulls.examples._game_state.GameState,
    space_shooter_scene: seagulls.engine._game_scene.IGameScene,
    seagulls_scene: seagulls.engine._game_scene.IGameScene,
    rpg_scene: seagulls.engine._game_scene.IGameScene
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
                    game_state: GameState,
                    space_shooter_scene: IGameScene,
                    seagulls_scene: IGameScene,
                    rpg_scene: IGameScene,):

                self._surface_renderer = surface_renderer
                self._asset_manager = asset_manager
                self._game_controls = game_controls
                self._game_state = game_state

                self._space_shooter_scene = space_shooter_scene
                self._seagulls_scene = seagulls_scene
                self._rpg_scene = rpg_scene

                self._game_objects = GameObjectsCollection()
                self._game_objects.add(background)
                self._space_shooter_menu_button = SpaceShooterMenuButton(
                    asset_manager=asset_manager,
                    game_controls=game_controls,
                )
                self._seagulls_menu_button = SeagullsMenuButton(
                    asset_manager=asset_manager,
                    game_controls=game_controls,
                )
                self._rpg_menu_button = RpgMenuButton(
                    asset_manager=asset_manager,
                    game_controls=game_controls,
                )

                self._game_objects.add(self._space_shooter_menu_button)
                self._game_objects.add(self._seagulls_menu_button)
                self._game_objects.add(self._rpg_menu_button)
                self._game_objects.add(self._game_controls)

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
                if self._space_shooter_menu_button.should_switch:
                    logger.debug("SWITCHING SCENE TO SPACE SHOOTER")
                    self._change_scene(self._space_shooter_scene)
                if self._seagulls_menu_button.should_switch:
                    logger.debug("SWITCHING SCENE TO SEAGULLS")
                    self._change_scene(self._seagulls_scene)
                if self._rpg_menu_button.should_switch:
                    logger.debug("SWITCHING SCENE TO RPG")
                    self._change_scene(self._rpg_scene)
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
            _active_scene: IGameScene
            _game_state: GameState

            def __init__(self, active_scene: IGameScene, game_state: GameState):
                self._active_scene = active_scene
                self._game_state = game_state
                self._game_state.active_scene = active_scene

            def start(self) -> None:
                self._active_scene.start()

            def should_quit(self) -> bool:
                return self._active_scene.should_quit()

            def tick(self) -> None:
                if self._game_state.game_state_changed:
                    self._update_scene()
                    self._active_scene.start()
                self._active_scene.tick()

            def _update_scene(self) -> None:
                self._active_scene = self._game_state.active_scene
                self._game_state.game_state_changed = False

    ```


### WindowScene()

```python
WindowScene(
    active_scene: seagulls.engine._game_scene.IGameScene,
    game_state: seagulls.examples._game_state.GameState
):
```


??? note "View Source"
    ```python
            def __init__(self, active_scene: IGameScene, game_state: GameState):
                self._active_scene = active_scene
                self._game_state = game_state
                self._game_state.active_scene = active_scene

    ```


### start()

```python
def start(self) -> None:
```


??? note "View Source"
    ```python
            def start(self) -> None:
                self._active_scene.start()

    ```


### should_quit()

```python
def should_quit(self) -> bool:
```


??? note "View Source"
    ```python
            def should_quit(self) -> bool:
                return self._active_scene.should_quit()

    ```


### tick()

```python
def tick(self) -> None:
```


??? note "View Source"
    ```python
            def tick(self) -> None:
                if self._game_state.game_state_changed:
                    self._update_scene()
                    self._active_scene.start()
                self._active_scene.tick()

    ```


## GameState

```python
class GameState:
```


??? note "View Source"
    ```python
        class GameState:
            active_scene: Optional[IGameScene] = None
            game_state_changed: bool = False

    ```


### GameState()

```python
GameState():
```




### active_scene

```python
active_scene: Optional[seagulls.engine._game_scene.IGameScene] = None
```



### game_state_changed

```python
game_state_changed: bool = False
```



