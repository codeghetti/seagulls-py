<div>
                ##[../seagulls](seagulls).examples
            
            !!! note "View Source"
    ```python
        from ._main_menu_scene import MainMenuScene
        from ._scene_manager import ExampleSceneManager
        from ._session import AsyncGameSession, BlockingGameSession
        from ._simple_stars_background import SimpleStarsBackground
        from ._simple_rpg_background import SimpleRpgBackground
        from ._window_scene import WindowScene
        from ._game_state import GameState

        __all__ = [
            &#34;MainMenuScene&#34;,
            &#34;AsyncGameSession&#34;,
            &#34;BlockingGameSession&#34;,
            &#34;ExampleSceneManager&#34;,
            &#34;SimpleStarsBackground&#34;,
            &#34;SimpleRpgBackground&#34;,
            &#34;WindowScene&#34;,
            &#34;GameState&#34;
        ]

    ```

                <section id="MainMenuScene">
                                <div class="attr class">
        <a class="headerlink" href="#MainMenuScene">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">MainMenuScene</span>- seagulls.engine._game_scene.IGameScene:
    </div>

        !!! note "View Source"
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

            def start(self) -&gt; None:
                self._surface_renderer.start()
                self.tick()

            def should_quit(self) -&gt; bool:
                return self._should_quit.is_set()

            def tick(self) -&gt; None:
                self._game_objects.apply(lambda x: x.tick())
                if self._space_shooter_menu_button.should_switch:
                    logger.debug(&#34;SWITCHING SCENE TO SPACE SHOOTER&#34;)
                    self._change_scene(self._space_shooter_scene)
                if self._seagulls_menu_button.should_switch:
                    logger.debug(&#34;SWITCHING SCENE TO SEAGULLS&#34;)
                    self._change_scene(self._seagulls_scene)
                if self._rpg_menu_button.should_switch:
                    logger.debug(&#34;SWITCHING SCENE TO RPG&#34;)
                    self._change_scene(self._rpg_scene)
                if self._game_controls.should_quit():
                    logger.debug(&#34;QUIT EVENT DETECTED&#34;)
                    self._should_quit.set()

                self._render()

            def _change_scene(self, next_scene: IGameScene) -&gt; None:
                self._game_state.active_scene = next_scene
                self._game_state.game_state_changed = True

            def _render(self) -&gt; None:
                background = Surface((1024, 600))
                self._game_objects.apply(lambda x: x.render(background))

                self._surface_renderer.render(background)

    ```

            This class is for X and Y.


                            <div id="MainMenuScene.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#MainMenuScene.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">MainMenuScene</span><span class="signature">(
    surface_renderer: <a href="engine.html#_surface_renderer.SurfaceRenderer">seagulls.engine._surface_renderer.SurfaceRenderer</a>,
    asset_manager: <a href="assets.html#_manager.AssetManager">seagulls.assets._manager.AssetManager</a>,
    background: <a href="engine.html#_game_object.GameObject">seagulls.engine._game_object.GameObject</a>,
    game_controls: <a href="engine.html#_game_controls.GameControls">seagulls.engine._game_controls.GameControls</a>,
    game_state: <a href="#_game_state.GameState">seagulls.examples._game_state.GameState</a>,
    space_shooter_scene: <a href="engine.html#_game_scene.IGameScene">seagulls.engine._game_scene.IGameScene</a>,
    seagulls_scene: <a href="engine.html#_game_scene.IGameScene">seagulls.engine._game_scene.IGameScene</a>,
    rpg_scene: <a href="engine.html#_game_scene.IGameScene">seagulls.engine._game_scene.IGameScene</a>
)</span>
    </div>

        !!! note "View Source"
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

    

                            </div>
                            <div id="MainMenuScene.start" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#MainMenuScene.start">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">start</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def start(self) -&gt; None:
                self._surface_renderer.start()
                self.tick()

    ```

    

                            </div>
                            <div id="MainMenuScene.should_quit" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#MainMenuScene.should_quit">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">should_quit</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def should_quit(self) -&gt; bool:
                return self._should_quit.is_set()

    ```

    

                            </div>
                            <div id="MainMenuScene.tick" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#MainMenuScene.tick">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">tick</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def tick(self) -&gt; None:
                self._game_objects.apply(lambda x: x.tick())
                if self._space_shooter_menu_button.should_switch:
                    logger.debug(&#34;SWITCHING SCENE TO SPACE SHOOTER&#34;)
                    self._change_scene(self._space_shooter_scene)
                if self._seagulls_menu_button.should_switch:
                    logger.debug(&#34;SWITCHING SCENE TO SEAGULLS&#34;)
                    self._change_scene(self._seagulls_scene)
                if self._rpg_menu_button.should_switch:
                    logger.debug(&#34;SWITCHING SCENE TO RPG&#34;)
                    self._change_scene(self._rpg_scene)
                if self._game_controls.should_quit():
                    logger.debug(&#34;QUIT EVENT DETECTED&#34;)
                    self._should_quit.set()

                self._render()

    ```

    

                            </div>
                </section>
                <section id="AsyncGameSession">
                                <div class="attr class">
        <a class="headerlink" href="#AsyncGameSession">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">AsyncGameSession</span>- seagulls.engine._game_session.IGameSession:
    </div>

        !!! note "View Source"
    ```python
        class AsyncGameSession(IGameSession):
            _scene_manager: IProvideGameScenes
            _thread: Thread
            _stopped: Event

            def __init__(self, scene_manager: IProvideGameScenes) -&gt; None:
                self._scene_manager = scene_manager

                self._thread = Thread(target=self._thread_target)
                self._stopped = Event()

            def start(self) -&gt; None:
                logger.debug(f&#34;starting game session&#34;)
                self._thread.start()

            def wait_for_completion(self) -&gt; None:
                logger.debug(f&#34;waiting for completion&#34;)
                while not self._stopped.is_set():
                    time.sleep(0.1)
                logger.debug(f&#34;done waiting for completion&#34;)

            def stop(self) -&gt; None:
                logger.debug(f&#34;stopping game session&#34;)
                self._stopped.set()
                self._thread.join()

            def _thread_target(self) -&gt; None:
                pygame.display.set_caption(&#34;Our Game&#34;)
                scene = self._scene_manager.get_scene()
                scene.start()

                while not self._stopped.is_set() and not scene.should_quit():
                    scene.tick()
                logger.debug(&#34;exiting game session&#34;)
                self._stopped.set()

    ```

            Helper class that provides a standard way to create an ABC using
inheritance.


                            <div id="AsyncGameSession.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#AsyncGameSession.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">AsyncGameSession</span><span class="signature">(
    scene_manager: <a href="engine.html#_game_scene_manager.IProvideGameScenes">seagulls.engine._game_scene_manager.IProvideGameScenes</a>
)</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self, scene_manager: IProvideGameScenes) -&gt; None:
                self._scene_manager = scene_manager

                self._thread = Thread(target=self._thread_target)
                self._stopped = Event()

    ```

    

                            </div>
                            <div id="AsyncGameSession.start" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#AsyncGameSession.start">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">start</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def start(self) -&gt; None:
                logger.debug(f&#34;starting game session&#34;)
                self._thread.start()

    ```

    

                            </div>
                            <div id="AsyncGameSession.wait_for_completion" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#AsyncGameSession.wait_for_completion">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">wait_for_completion</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def wait_for_completion(self) -&gt; None:
                logger.debug(f&#34;waiting for completion&#34;)
                while not self._stopped.is_set():
                    time.sleep(0.1)
                logger.debug(f&#34;done waiting for completion&#34;)

    ```

    

                            </div>
                            <div id="AsyncGameSession.stop" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#AsyncGameSession.stop">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">stop</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def stop(self) -&gt; None:
                logger.debug(f&#34;stopping game session&#34;)
                self._stopped.set()
                self._thread.join()

    ```

    

                            </div>
                </section>
                <section id="BlockingGameSession">
                                <div class="attr class">
        <a class="headerlink" href="#BlockingGameSession">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">BlockingGameSession</span>- seagulls.engine._game_session.IGameSession:
    </div>

        !!! note "View Source"
    ```python
        class BlockingGameSession(IGameSession):
            _scene_manager: IProvideGameScenes

            def __init__(self, scene_manager: IProvideGameScenes) -&gt; None:
                self._scene_manager = scene_manager

            def start(self) -&gt; None:
                logger.debug(f&#34;starting game session&#34;)
                pygame.display.set_caption(&#34;Our Game&#34;)
                scene = self._scene_manager.get_scene()
                scene.start()

                while not scene.should_quit():
                    scene.tick()
                logger.debug(&#34;exiting game session&#34;)

            def wait_for_completion(self) -&gt; None:
                pass

            def stop(self) -&gt; None:
                pass

    ```

            Helper class that provides a standard way to create an ABC using
inheritance.


                            <div id="BlockingGameSession.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#BlockingGameSession.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">BlockingGameSession</span><span class="signature">(
    scene_manager: <a href="engine.html#_game_scene_manager.IProvideGameScenes">seagulls.engine._game_scene_manager.IProvideGameScenes</a>
)</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self, scene_manager: IProvideGameScenes) -&gt; None:
                self._scene_manager = scene_manager

    ```

    

                            </div>
                            <div id="BlockingGameSession.start" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#BlockingGameSession.start">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">start</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def start(self) -&gt; None:
                logger.debug(f&#34;starting game session&#34;)
                pygame.display.set_caption(&#34;Our Game&#34;)
                scene = self._scene_manager.get_scene()
                scene.start()

                while not scene.should_quit():
                    scene.tick()
                logger.debug(&#34;exiting game session&#34;)

    ```

    

                            </div>
                            <div id="BlockingGameSession.wait_for_completion" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#BlockingGameSession.wait_for_completion">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">wait_for_completion</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def wait_for_completion(self) -&gt; None:
                pass

    ```

    

                            </div>
                            <div id="BlockingGameSession.stop" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#BlockingGameSession.stop">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">stop</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def stop(self) -&gt; None:
                pass

    ```

    

                            </div>
                </section>
                <section id="ExampleSceneManager">
                                <div class="attr class">
        <a class="headerlink" href="#ExampleSceneManager">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">ExampleSceneManager</span>- seagulls.engine._game_scene_manager.IProvideGameScenes:
    </div>

        !!! note "View Source"
    ```python
        class ExampleSceneManager(IProvideGameScenes):
            _scene: MainMenuScene

            def __init__(self, scene: MainMenuScene):
                self._scene = scene

            def get_scene(self) -&gt; IGameScene:
                return self._scene

    ```

            Helper class that provides a standard way to create an ABC using
inheritance.


                            <div id="ExampleSceneManager.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#ExampleSceneManager.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">ExampleSceneManager</span><span class="signature">(scene: <a href="#_main_menu_scene.MainMenuScene">seagulls.examples._main_menu_scene.MainMenuScene</a>)</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self, scene: MainMenuScene):
                self._scene = scene

    ```

    

                            </div>
                            <div id="ExampleSceneManager.get_scene" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#ExampleSceneManager.get_scene">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_scene</span><span class="signature">(self) -&gt; <a href="engine.html#_game_scene.IGameScene">seagulls.engine._game_scene.IGameScene</a></span>:
    </div>

        !!! note "View Source"
    ```python
            def get_scene(self) -&gt; IGameScene:
                return self._scene

    ```

    

                            </div>
                </section>
                <section id="SimpleStarsBackground">
                                <div class="attr class">
        <a class="headerlink" href="#SimpleStarsBackground">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">SimpleStarsBackground</span>- seagulls.engine._game_object.GameObject:
    </div>

        !!! note "View Source"
    ```python
        class SimpleStarsBackground(GameObject):

            _asset_manager: AssetManager

            def __init__(self, asset_manager: AssetManager):
                self._asset_manager = asset_manager

            def tick(self) -&gt; None:
                pass

            def render(self, surface: Surface) -&gt; None:
                background = self._get_cached_background()
                surface.blit(background, (0, 0))

            @lru_cache()
            def _get_cached_background(self) -&gt; Surface:
                return self._asset_manager.load_sprite(&#34;environment/environment-stars&#34;).copy()

    ```

            Interface for anything representing an object in the scene.


                            <div id="SimpleStarsBackground.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#SimpleStarsBackground.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">SimpleStarsBackground</span><span class="signature">(asset_manager: <a href="assets.html#_manager.AssetManager">seagulls.assets._manager.AssetManager</a>)</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self, asset_manager: AssetManager):
                self._asset_manager = asset_manager

    ```

    

                            </div>
                            <div id="SimpleStarsBackground.tick" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#SimpleStarsBackground.tick">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">tick</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def tick(self) -&gt; None:
                pass

    ```

    

                            </div>
                            <div id="SimpleStarsBackground.render" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#SimpleStarsBackground.render">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">render</span><span class="signature">(self, surface: pygame.Surface) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def render(self, surface: Surface) -&gt; None:
                background = self._get_cached_background()
                surface.blit(background, (0, 0))

    ```

    

                            </div>
                </section>
                <section id="SimpleRpgBackground">
                                <div class="attr class">
        <a class="headerlink" href="#SimpleRpgBackground">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">SimpleRpgBackground</span>- seagulls.engine._game_object.GameObject:
    </div>

        !!! note "View Source"
    ```python
        class SimpleRpgBackground(GameObject):

            _asset_manager: AssetManager
            _game_board: GameBoard

            def __init__(self, asset_manager: AssetManager):
                self._asset_manager = asset_manager
                self._game_board = GameBoard()

            def tick(self) -&gt; None:
                pass

            def render(self, surface: Surface) -&gt; None:
                background = self._get_cached_background()
                surface.blit(background, (0, 0))

            @lru_cache()
            def _get_cached_background(self) -&gt; Surface:
                surface = Surface((1024, 600))

                top_left_corner = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-top-left-corner&#34;).copy()
                top_island_edge = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-top-edge&#34;).copy()
                top_right_corner = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-top-right-corner&#34;).copy()
                island_water = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-water&#34;).copy()
                bottom_left_corner = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-bottom-left-corner&#34;).copy()
                bottom_island_edge = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-bottom-edge&#34;).copy()
                bottom_right_corner = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-bottom-right-corner&#34;).copy()
                island_left_edge = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-left-edge&#34;).copy()
                island_right_edge = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-right-edge&#34;).copy()
                island_grass = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-grass&#34;).copy()
                island_red_home = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-red-home&#34;).copy()
                island_blue_home = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-blue-home&#34;).copy()
                island_tree = self._asset_manager.load_sprite(
                    &#34;environment/rpg-environment/island-tree&#34;).copy()

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
                            if random_number &lt; 92:
                                surface.blit(island_grass, (x * 16, y * 16))
                            elif random_number &lt; 93:
                                if len(self._game_board.get_neighbors(x * 16, y * 16, 16)) == 0:
                                    surface.blit(island_red_home, (x * 16, y * 16))
                                    self._game_board.set_tile(x * 16, y * 16, Tile())
                                else:
                                    surface.blit(island_grass, (x * 16, y * 16))
                            elif random_number &lt; 94:
                                if len(self._game_board.get_neighbors(x * 16, y * 16, 16)) == 0:
                                    surface.blit(island_blue_home, (x * 16, y * 16))
                                    self._game_board.set_tile(x * 16, y * 16, Tile())
                                else:
                                    surface.blit(island_grass, (x * 16, y * 16))
                            else:
                                surface.blit(island_tree, (x * 16, y * 16))
                return surface

    ```

            Interface for anything representing an object in the scene.


                            <div id="SimpleRpgBackground.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#SimpleRpgBackground.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">SimpleRpgBackground</span><span class="signature">(asset_manager: <a href="assets.html#_manager.AssetManager">seagulls.assets._manager.AssetManager</a>)</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self, asset_manager: AssetManager):
                self._asset_manager = asset_manager
                self._game_board = GameBoard()

    ```

    

                            </div>
                            <div id="SimpleRpgBackground.tick" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#SimpleRpgBackground.tick">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">tick</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def tick(self) -&gt; None:
                pass

    ```

    

                            </div>
                            <div id="SimpleRpgBackground.render" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#SimpleRpgBackground.render">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">render</span><span class="signature">(self, surface: pygame.Surface) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def render(self, surface: Surface) -&gt; None:
                background = self._get_cached_background()
                surface.blit(background, (0, 0))

    ```

    

                            </div>
                </section>
                <section id="WindowScene">
                                <div class="attr class">
        <a class="headerlink" href="#WindowScene">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">WindowScene</span>- seagulls.engine._game_scene.IGameScene:
    </div>

        !!! note "View Source"
    ```python
        class WindowScene(IGameScene):
            _active_scene: IGameScene
            _game_state: GameState

            def __init__(self, active_scene: IGameScene, game_state: GameState):
                self._active_scene = active_scene
                self._game_state = game_state
                self._game_state.active_scene = active_scene

            def start(self) -&gt; None:
                self._active_scene.start()

            def should_quit(self) -&gt; bool:
                return self._active_scene.should_quit()

            def tick(self) -&gt; None:
                if self._game_state.game_state_changed:
                    self._update_scene()
                    self._active_scene.start()
                self._active_scene.tick()

            def _update_scene(self) -&gt; None:
                self._active_scene = self._game_state.active_scene
                self._game_state.game_state_changed = False

    ```

            This class is for X and Y.


                            <div id="WindowScene.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#WindowScene.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">WindowScene</span><span class="signature">(
    active_scene: <a href="engine.html#_game_scene.IGameScene">seagulls.engine._game_scene.IGameScene</a>,
    game_state: <a href="#_game_state.GameState">seagulls.examples._game_state.GameState</a>
)</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self, active_scene: IGameScene, game_state: GameState):
                self._active_scene = active_scene
                self._game_state = game_state
                self._game_state.active_scene = active_scene

    ```

    

                            </div>
                            <div id="WindowScene.start" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#WindowScene.start">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">start</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def start(self) -&gt; None:
                self._active_scene.start()

    ```

    

                            </div>
                            <div id="WindowScene.should_quit" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#WindowScene.should_quit">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">should_quit</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def should_quit(self) -&gt; bool:
                return self._active_scene.should_quit()

    ```

    

                            </div>
                            <div id="WindowScene.tick" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#WindowScene.tick">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">tick</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def tick(self) -&gt; None:
                if self._game_state.game_state_changed:
                    self._update_scene()
                    self._active_scene.start()
                self._active_scene.tick()

    ```

    

                            </div>
                </section>
                <section id="GameState">
                                <div class="attr class">
        <a class="headerlink" href="#GameState">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">GameState</span>:
    </div>

        !!! note "View Source"
    ```python
        class GameState:
            active_scene: Optional[IGameScene] = None
            game_state_changed: bool = False

    ```

    

                            <div id="GameState.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameState.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">GameState</span><span class="signature">()</span>
    </div>

        
    

                            </div>
                            <div id="GameState.active_scene" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#GameState.active_scene">#&nbsp;&nbsp</a>

        <span class="name">active_scene</span><span class="annotation">: Optional[<a href="engine.html#_game_scene.IGameScene">seagulls.engine._game_scene.IGameScene</a>]</span><span class="default_value"> = None</span>
    </div>

    

                            </div>
                            <div id="GameState.game_state_changed" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#GameState.game_state_changed">#&nbsp;&nbsp</a>

        <span class="name">game_state_changed</span><span class="annotation">: bool</span><span class="default_value"> = False</span>
    </div>

    

                            </div>
                </section>
    </main>
<script>
    function escapeHTML(html) {
        return document.createElement('div').appendChild(document.createTextNode(html)).parentNode.innerHTML;
    }

    const originalContent = document.querySelector("main.pdoc");
    let currentContent = originalContent;

    function setContent(innerHTML) {
        let elem;
        if (innerHTML) {
            elem = document.createElement("main");
            elem.classList.add("pdoc");
            elem.innerHTML = innerHTML;
        } else {
            elem = originalContent;
        }
        if (currentContent !== elem) {
            currentContent.replaceWith(elem);
            currentContent = elem;
        }
    }

    function getSearchTerm() {
        return (new URL(window.location)).searchParams.get("search");
    }

    const searchBox = document.querySelector(".pdoc input[type=search]");
    searchBox.addEventListener("input", function () {
        let url = new URL(window.location);
        if (searchBox.value.trim()) {
            url.hash = "";
            url.searchParams.set("search", searchBox.value);
        } else {
            url.searchParams.delete("search");
        }
        history.replaceState("", "", url.toString());
        onInput();
    });
    window.addEventListener("popstate", onInput);


    let search, searchErr;

    async function initialize() {
        try {
            search = await new Promise((resolve, reject) => {
                const script = document.createElement("script");
                script.type = "text/javascript";
                script.async = true;
                script.onload = () => resolve(window.pdocSearch);
                script.onerror = (e) => reject(e);
                script.src = "../search.js";
                document.getElementsByTagName("head")[0].appendChild(script);
            });
        } catch (e) {
            console.error("Cannot fetch pdoc search index");
            searchErr = "Cannot fetch search index.";
        }
        onInput();

        document.querySelector("nav.pdoc").addEventListener("click", e => {
            if (e.target.hash) {
                searchBox.value = "";
                searchBox.dispatchEvent(new Event("input"));
            }
        });
    }

    function onInput() {
        setContent((() => {
            const term = getSearchTerm();
            if (!term) {
                return null
            }
            if (searchErr) {
                return `<h3>Error: ${searchErr}</h3>`
            }
            if (!search) {
                return "<h3>Searching...</h3>"
            }

            window.scrollTo({top: 0, left: 0, behavior: 'auto'});

            const results = search(term);

            let html;
            if (results.length === 0) {
                html = `No search results for '${escapeHTML(term)}'.`
            } else {
                html = `<h4>${results.length} search result${results.length > 1 ? "s" : ""} for '${escapeHTML(term)}'.</h4>`;
            }
            for (let result of results.slice(0, 10)) {
                let doc = result.doc;
                let url = `../${doc.modulename.replaceAll(".", "/")}.html`;
                if (doc.qualname) {
                    url += `#${doc.qualname}`;
                }

                let heading;
                switch (result.doc.type) {
                    case "function":
                        heading = `<span class="def">${doc.funcdef}</span> <span class="name">${doc.fullname}</span><span class="signature">(${doc.parameters.join(", ")})</span>`;
                        break;
                    case "class":
                        heading = `<span class="def">class</span> <span class="name">${doc.fullname}</span>`;
                        break;
                    default:
                        heading = `<span class="name">${doc.fullname}</span>`;
                        break;
                }
                html += `
                        <section class="search-result">
                        <a href="${url}" class="attr ${doc.type}">${heading}</a>
                        <div class="docstring">${doc.doc}</div>
                        </section>
                    `;

            }
            return html;
        })());
    }

    if (getSearchTerm()) {
        initialize();
        searchBox.value = getSearchTerm();
        onInput();
    } else {
        searchBox.addEventListener("focus", initialize, {once: true});
    }

    searchBox.addEventListener("keydown", e => {
        if (["ArrowDown", "ArrowUp", "Enter"].includes(e.key)) {
            let focused = currentContent.querySelector(".search-result.focused");
            if (!focused) {
                currentContent.querySelector(".search-result").classList.add("focused");
            } else if (
                e.key === "ArrowDown"
                && focused.nextElementSibling
                && focused.nextElementSibling.classList.contains("search-result")
            ) {
                focused.classList.remove("focused");
                focused.nextElementSibling.classList.add("focused");
                focused.nextElementSibling.scrollIntoView({
                    behavior: "smooth",
                    block: "nearest",
                    inline: "nearest"
                });
            } else if (
                e.key === "ArrowUp"
                && focused.previousElementSibling
                && focused.previousElementSibling.classList.contains("search-result")
            ) {
                focused.classList.remove("focused");
                focused.previousElementSibling.classList.add("focused");
                focused.previousElementSibling.scrollIntoView({
                    behavior: "smooth",
                    block: "nearest",
                    inline: "nearest"
                });
            } else if (
                e.key === "Enter"
            ) {
                focused.querySelector("a").click();
            }
        }
    });
</script></div>