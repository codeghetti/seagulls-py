<div>
                ##[../seagulls](seagulls).engine
                    Core Engine Components

            !!! note "View Source"
    ```python
        &#34;&#34;&#34;Core Engine Components&#34;&#34;&#34;
        from ._collisions import CollidableObject, flag_from_string
        from ._game_clock import GameClock
        from ._game_controls import GameControls
        from ._game_object import GameObject, GameObjectsCollection
        from ._game_scene import IGameScene
        from ._game_scene_manager import IProvideGameScenes
        from ._game_session import IGameSession
        from ._game_session_manager import IProvideGameSessions
        from ._game_settings import GameSettings
        from ._pyagme import Color, PixelArray, Rect, Surface, Vector2, Vector3
        from ._surface_renderer import SurfaceRenderer

        __all__ = [
            &#34;flag_from_string&#34;,
            &#34;CollidableObject&#34;,
            &#34;IGameScene&#34;,
            &#34;IProvideGameScenes&#34;,
            &#34;IProvideGameSessions&#34;,
            &#34;IGameSession&#34;,
            &#34;SurfaceRenderer&#34;,
            &#34;GameClock&#34;,
            &#34;GameControls&#34;,
            &#34;GameObject&#34;,
            &#34;GameObjectsCollection&#34;,
            &#34;GameSettings&#34;,
            &#34;Rect&#34;,
            &#34;Surface&#34;,
            &#34;Color&#34;,
            &#34;PixelArray&#34;,
            &#34;Vector2&#34;,
            &#34;Vector3&#34;,
        ]

    ```

                <section id="flag_from_string">
                            <div class="attr function"><a class="headerlink" href="#flag_from_string">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">flag_from_string</span><span class="signature">(value: str) -&gt; int</span>:
    </div>

        !!! note "View Source"
    ```python
        def flag_from_string(value: str) -&gt; int:
            if not isinstance(value, str):
                raise ValueError(f&#34;Value must be a string of 0s and 1s: {value}&#34;)

            return int(value, 2)

    ```

    

                </section>
                <section id="CollidableObject">
                                <div class="attr class">
        <a class="headerlink" href="#CollidableObject">#&nbsp;&nbsp</a>

                <div class="decorator">@dataclass(frozen=True)</div>

        <span class="def">class</span>
        <span class="name">CollidableObject</span>:
    </div>

        !!! note "View Source"
    ```python
        @dataclass(frozen=True)
        class CollidableObject:
            layer: int
            mask: int

            def filter_by_mask(
                    self, targets: Tuple[&#34;CollidableObject&#34;, ...]) -&gt; Tuple[&#34;CollidableObject&#34;, ...]:
                result = []
                for t in targets:
                    if self.is_in_mask(t):
                        result.append(t)

                return tuple(result)

            def is_in_mask(self, target: &#34;CollidableObject&#34;) -&gt; bool:
                logger.debug(f&#34;targeting items located in mask: {self.mask:b}&#34;)
                logger.debug(f&#34;target is located in layer: {target.layer:b}&#34;)
                logger.debug(f&#34;&amp; result: {self.mask &amp; target.layer:b}&#34;)
                return self.mask &amp; target.layer &gt; 0

            def __repr__(self) -&gt; str:
                return f&#34;{self.__class__.__name__}(layer={self.layer:b}, mask={self.mask:b})&#34;

    ```

            CollidableObject(layer: int, mask: int)


                            <div id="CollidableObject.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#CollidableObject.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">CollidableObject</span><span class="signature">(layer: int, mask: int)</span>
    </div>

        
    

                            </div>
                            <div id="CollidableObject.filter_by_mask" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#CollidableObject.filter_by_mask">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">filter_by_mask</span><span class="signature">(
    self,
    targets: Tuple[<a href="#_collisions.CollidableObject">seagulls.engine._collisions.CollidableObject</a>, ...]
) -&gt; Tuple[<a href="#_collisions.CollidableObject">seagulls.engine._collisions.CollidableObject</a>, ...]</span>:
    </div>

        !!! note "View Source"
    ```python
            def filter_by_mask(
                    self, targets: Tuple[&#34;CollidableObject&#34;, ...]) -&gt; Tuple[&#34;CollidableObject&#34;, ...]:
                result = []
                for t in targets:
                    if self.is_in_mask(t):
                        result.append(t)

                return tuple(result)

    ```

    

                            </div>
                            <div id="CollidableObject.is_in_mask" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#CollidableObject.is_in_mask">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">is_in_mask</span><span class="signature">(self, target: <a href="#_collisions.CollidableObject">seagulls.engine._collisions.CollidableObject</a>) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def is_in_mask(self, target: &#34;CollidableObject&#34;) -&gt; bool:
                logger.debug(f&#34;targeting items located in mask: {self.mask:b}&#34;)
                logger.debug(f&#34;target is located in layer: {target.layer:b}&#34;)
                logger.debug(f&#34;&amp; result: {self.mask &amp; target.layer:b}&#34;)
                return self.mask &amp; target.layer &gt; 0

    ```

    

                            </div>
                </section>
                <section id="IGameScene">
                                <div class="attr class">
        <a class="headerlink" href="#IGameScene">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">IGameScene</span>- abc.ABC:
    </div>

        !!! note "View Source"
    ```python
        class IGameScene(ABC):
            &#34;&#34;&#34;
            This class is for X and Y.
            &#34;&#34;&#34;

            @abstractmethod
            def start(self) -&gt; None:
                pass

            @abstractmethod
            def should_quit(self) -&gt; bool:
                pass

            @abstractmethod
            def tick(self) -&gt; None:
                pass

    ```

            This class is for X and Y.


                            <div id="IGameScene.start" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#IGameScene.start">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">start</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def start(self) -&gt; None:
                pass

    ```

    

                            </div>
                            <div id="IGameScene.should_quit" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#IGameScene.should_quit">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">should_quit</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def should_quit(self) -&gt; bool:
                pass

    ```

    

                            </div>
                            <div id="IGameScene.tick" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#IGameScene.tick">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">tick</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def tick(self) -&gt; None:
                pass

    ```

    

                            </div>
                </section>
                <section id="IProvideGameScenes">
                                <div class="attr class">
        <a class="headerlink" href="#IProvideGameScenes">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">IProvideGameScenes</span>- abc.ABC:
    </div>

        !!! note "View Source"
    ```python
        class IProvideGameScenes(ABC):

            @abstractmethod
            def get_scene(self) -&gt; IGameScene:
                pass

    ```

            Helper class that provides a standard way to create an ABC using
inheritance.


                            <div id="IProvideGameScenes.get_scene" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#IProvideGameScenes.get_scene">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">get_scene</span><span class="signature">(self) -&gt; <a href="#_game_scene.IGameScene">seagulls.engine._game_scene.IGameScene</a></span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def get_scene(self) -&gt; IGameScene:
                pass

    ```

    

                            </div>
                </section>
                <section id="IProvideGameSessions">
                                <div class="attr class">
        <a class="headerlink" href="#IProvideGameSessions">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">IProvideGameSessions</span>- abc.ABC:
    </div>

        !!! note "View Source"
    ```python
        class IProvideGameSessions(ABC):

            @abstractmethod
            def get_session(self, scene: str) -&gt; IGameSession:
                pass

    ```

            Helper class that provides a standard way to create an ABC using
inheritance.


                            <div id="IProvideGameSessions.get_session" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#IProvideGameSessions.get_session">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">get_session</span><span class="signature">(self, scene: str) -&gt; <a href="#_game_session.IGameSession">seagulls.engine._game_session.IGameSession</a></span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def get_session(self, scene: str) -&gt; IGameSession:
                pass

    ```

    

                            </div>
                </section>
                <section id="IGameSession">
                                <div class="attr class">
        <a class="headerlink" href="#IGameSession">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">IGameSession</span>- abc.ABC:
    </div>

        !!! note "View Source"
    ```python
        class IGameSession(ABC):

            @abstractmethod
            def start(self) -&gt; None:
                pass

            @abstractmethod
            def wait_for_completion(self) -&gt; None:
                pass

            @abstractmethod
            def stop(self) -&gt; None:
                pass

    ```

            Helper class that provides a standard way to create an ABC using
inheritance.


                            <div id="IGameSession.start" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#IGameSession.start">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">start</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def start(self) -&gt; None:
                pass

    ```

    

                            </div>
                            <div id="IGameSession.wait_for_completion" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#IGameSession.wait_for_completion">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">wait_for_completion</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def wait_for_completion(self) -&gt; None:
                pass

    ```

    

                            </div>
                            <div id="IGameSession.stop" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#IGameSession.stop">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">stop</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def stop(self) -&gt; None:
                pass

    ```

    

                            </div>
                </section>
                <section id="SurfaceRenderer">
                                <div class="attr class">
        <a class="headerlink" href="#SurfaceRenderer">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">SurfaceRenderer</span>:
    </div>

        !!! note "View Source"
    ```python
        class SurfaceRenderer:
            def start(self) -&gt; None:
                self._get_surface()

            def render(self, surface: Surface) -&gt; None:
                self._get_surface().blit(surface, (0, 0))
                pygame.display.flip()

            @lru_cache()
            def _get_surface(self) -&gt; Surface:
                return pygame.display.set_mode((1024, 600))

    ```

    

                            <div id="SurfaceRenderer.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#SurfaceRenderer.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">SurfaceRenderer</span><span class="signature">()</span>
    </div>

        
    

                            </div>
                            <div id="SurfaceRenderer.start" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#SurfaceRenderer.start">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">start</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def start(self) -&gt; None:
                self._get_surface()

    ```

    

                            </div>
                            <div id="SurfaceRenderer.render" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#SurfaceRenderer.render">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">render</span><span class="signature">(self, surface: pygame.Surface) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def render(self, surface: Surface) -&gt; None:
                self._get_surface().blit(surface, (0, 0))
                pygame.display.flip()

    ```

    

                            </div>
                </section>
                <section id="GameClock">
                                <div class="attr class">
        <a class="headerlink" href="#GameClock">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">GameClock</span>- <a href="#GameObject">seagulls.engine.GameObject</a>:
    </div>

        !!! note "View Source"
    ```python
        class GameClock(GameObject):
            _clock: Clock
            _ticks: int
            _delta: int

            def __init__(self):
                self._clock = Clock()
                self._ticks = 0
                self._delta = 0

            def tick(self) -&gt; None:
                self._delta = self._clock.tick()

            def render(self, surface: Surface) -&gt; None:
                pass

            def get_time(self) -&gt; int:
                return self._delta

            def get_fps(self) -&gt; float:
                return self._clock.get_fps()

    ```

            Interface for anything representing an object in the scene.


                            <div id="GameClock.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameClock.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">GameClock</span><span class="signature">()</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self):
                self._clock = Clock()
                self._ticks = 0
                self._delta = 0

    ```

    

                            </div>
                            <div id="GameClock.tick" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameClock.tick">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">tick</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def tick(self) -&gt; None:
                self._delta = self._clock.tick()

    ```

    

                            </div>
                            <div id="GameClock.render" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameClock.render">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">render</span><span class="signature">(self, surface: pygame.Surface) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def render(self, surface: Surface) -&gt; None:
                pass

    ```

    

                            </div>
                            <div id="GameClock.get_time" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameClock.get_time">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_time</span><span class="signature">(self) -&gt; int</span>:
    </div>

        !!! note "View Source"
    ```python
            def get_time(self) -&gt; int:
                return self._delta

    ```

    

                            </div>
                            <div id="GameClock.get_fps" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameClock.get_fps">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_fps</span><span class="signature">(self) -&gt; float</span>:
    </div>

        !!! note "View Source"
    ```python
            def get_fps(self) -&gt; float:
                return self._clock.get_fps()

    ```

    

                            </div>
                </section>
                <section id="GameControls">
                                <div class="attr class">
        <a class="headerlink" href="#GameControls">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">GameControls</span>- <a href="#GameObject">seagulls.engine.GameObject</a>:
    </div>

        !!! note "View Source"
    ```python
        class GameControls(GameObject):

            _events: List[Event]

            def __init__(self):
                self._events = []

            def tick(self):
                self._events = pygame.event.get()

            def should_quit(self) -&gt; bool:
                for event in self._events:
                    if event.type == pygame.QUIT:
                        return True

                    if self._is_key_down_event(event, pygame.K_ESCAPE):
                        return True

                return False

            def should_fire(self) -&gt; bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_SPACE):
                        return True

                return False

            def is_left_moving(self) -&gt; bool:
                return pygame.key.get_pressed()[pygame.K_LEFT]

            def is_right_moving(self) -&gt; bool:
                return pygame.key.get_pressed()[pygame.K_RIGHT]

            def should_toggle_debug_hud(self) -&gt; bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_BACKQUOTE):
                        return True

                return False

            def is_click_initialized(self) -&gt; bool:
                for event in self._events:
                    if not event.type == pygame.MOUSEBUTTONDOWN:
                        continue

                    return pygame.mouse.get_pressed(num_buttons=3)[0]

                return False

            def is_mouse_down(self) -&gt; bool:
                return pygame.mouse.get_pressed(num_buttons=3)[0]

            def _is_key_down_event(self, event: Event, key: int) -&gt; bool:
                return event.type == pygame.KEYDOWN and event.key == key

            def _is_key_up_event(self, event: Event, key: int) -&gt; bool:
                return event.type == pygame.KEYUP and event.key == key

            def render(self, surface: pygame.Surface) -&gt; None:
                pass

    ```

            Interface for anything representing an object in the scene.


                            <div id="GameControls.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">GameControls</span><span class="signature">()</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self):
                self._events = []

    ```

    

                            </div>
                            <div id="GameControls.tick" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.tick">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">tick</span><span class="signature">(self)</span>:
    </div>

        !!! note "View Source"
    ```python
            def tick(self):
                self._events = pygame.event.get()

    ```

    

                            </div>
                            <div id="GameControls.should_quit" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.should_quit">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">should_quit</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def should_quit(self) -&gt; bool:
                for event in self._events:
                    if event.type == pygame.QUIT:
                        return True

                    if self._is_key_down_event(event, pygame.K_ESCAPE):
                        return True

                return False

    ```

    

                            </div>
                            <div id="GameControls.should_fire" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.should_fire">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">should_fire</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def should_fire(self) -&gt; bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_SPACE):
                        return True

                return False

    ```

    

                            </div>
                            <div id="GameControls.is_left_moving" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.is_left_moving">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">is_left_moving</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def is_left_moving(self) -&gt; bool:
                return pygame.key.get_pressed()[pygame.K_LEFT]

    ```

    

                            </div>
                            <div id="GameControls.is_right_moving" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.is_right_moving">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">is_right_moving</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def is_right_moving(self) -&gt; bool:
                return pygame.key.get_pressed()[pygame.K_RIGHT]

    ```

    

                            </div>
                            <div id="GameControls.should_toggle_debug_hud" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.should_toggle_debug_hud">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">should_toggle_debug_hud</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def should_toggle_debug_hud(self) -&gt; bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_BACKQUOTE):
                        return True

                return False

    ```

    

                            </div>
                            <div id="GameControls.is_click_initialized" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.is_click_initialized">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">is_click_initialized</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def is_click_initialized(self) -&gt; bool:
                for event in self._events:
                    if not event.type == pygame.MOUSEBUTTONDOWN:
                        continue

                    return pygame.mouse.get_pressed(num_buttons=3)[0]

                return False

    ```

    

                            </div>
                            <div id="GameControls.is_mouse_down" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.is_mouse_down">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">is_mouse_down</span><span class="signature">(self) -&gt; bool</span>:
    </div>

        !!! note "View Source"
    ```python
            def is_mouse_down(self) -&gt; bool:
                return pygame.mouse.get_pressed(num_buttons=3)[0]

    ```

    

                            </div>
                            <div id="GameControls.render" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameControls.render">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">render</span><span class="signature">(self, surface: pygame.Surface) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def render(self, surface: pygame.Surface) -&gt; None:
                pass

    ```

    

                            </div>
                </section>
                <section id="GameObject">
                                <div class="attr class">
        <a class="headerlink" href="#GameObject">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">GameObject</span>- abc.ABC:
    </div>

        !!! note "View Source"
    ```python
        class GameObject(ABC):
            &#34;&#34;&#34;
            Interface for anything representing an object in the scene.
            &#34;&#34;&#34;

            @abstractmethod
            def tick(self) -&gt; None:
                pass

            @abstractmethod
            def render(self, surface: Surface) -&gt; None:
                pass

    ```

            Interface for anything representing an object in the scene.


                            <div id="GameObject.tick" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameObject.tick">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">tick</span><span class="signature">(self) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def tick(self) -&gt; None:
                pass

    ```

    

                            </div>
                            <div id="GameObject.render" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameObject.render">#&nbsp;&nbsp</a>

                <div class="decorator">@abstractmethod</div>

            <span class="def">def</span>
            <span class="name">render</span><span class="signature">(self, surface: pygame.Surface) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            @abstractmethod
            def render(self, surface: Surface) -&gt; None:
                pass

    ```

    

                            </div>
                </section>
                <section id="GameObjectsCollection">
                                <div class="attr class">
        <a class="headerlink" href="#GameObjectsCollection">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">GameObjectsCollection</span>:
    </div>

        !!! note "View Source"
    ```python
        class GameObjectsCollection:
            &#34;&#34;&#34;
            Data structure that allows you to keep track of objects in the scene.
            &#34;&#34;&#34;

            _game_objects: List[GameObject]

            def __init__(self) -&gt; None:
                self._game_objects = []

            def add(self, game_object: GameObject) -&gt; None:
                self._game_objects.append(game_object)

            def apply(self, func: Callable[[GameObject], None]) -&gt; None:
                for game_object in self._game_objects:
                    func(game_object)

    ```

            Data structure that allows you to keep track of objects in the scene.


                            <div id="GameObjectsCollection.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameObjectsCollection.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">GameObjectsCollection</span><span class="signature">()</span>
    </div>

        !!! note "View Source"
    ```python
            def __init__(self) -&gt; None:
                self._game_objects = []

    ```

    

                            </div>
                            <div id="GameObjectsCollection.add" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameObjectsCollection.add">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">add</span><span class="signature">(self, game_object: <a href="#_game_object.GameObject">seagulls.engine._game_object.GameObject</a>) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def add(self, game_object: GameObject) -&gt; None:
                self._game_objects.append(game_object)

    ```

    

                            </div>
                            <div id="GameObjectsCollection.apply" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameObjectsCollection.apply">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">apply</span><span class="signature">(
    self,
    func: Callable[[<a href="#_game_object.GameObject">seagulls.engine._game_object.GameObject</a>], NoneType]
) -&gt; None</span>:
    </div>

        !!! note "View Source"
    ```python
            def apply(self, func: Callable[[GameObject], None]) -&gt; None:
                for game_object in self._game_objects:
                    func(game_object)

    ```

    

                            </div>
                </section>
                <section id="GameSettings">
                                <div class="attr class">
        <a class="headerlink" href="#GameSettings">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">GameSettings</span>:
    </div>

        !!! note "View Source"
    ```python
        class GameSettings:

            def get_setting(self, name, default=None) -&gt; Any:
                data = self._load_yaml()
                return data.get(name, default)

            @lru_cache()
            def _load_yaml(self) -&gt; Dict[str, Any]:
                file = Path.home() / &#34;.config/seagulls.yaml&#34;
                if not file.exists():
                    file.touch()

                return yaml.safe_load(file.read_text()) or {}

    ```

    

                            <div id="GameSettings.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameSettings.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">GameSettings</span><span class="signature">()</span>
    </div>

        
    

                            </div>
                            <div id="GameSettings.get_setting" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#GameSettings.get_setting">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_setting</span><span class="signature">(self, name, default=None) -&gt; Any</span>:
    </div>

        !!! note "View Source"
    ```python
            def get_setting(self, name, default=None) -&gt; Any:
                data = self._load_yaml()
                return data.get(name, default)

    ```

    

                            </div>
                </section>
                <section id="Rect">
                                <div class="attr class">
        <a class="headerlink" href="#Rect">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">Rect</span>:
    </div>

        
            Rect(left, top, width, height) -> Rect
Rect((left, top), (width, height)) -> Rect
Rect(object) -> Rect
pygame object for storing rectangular coordinates


                            <div id="Rect.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">Rect</span><span class="signature">(*args, **kwargs)</span>
    </div>

        
    

                            </div>
                            <div id="Rect.normalize" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.normalize">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">normalize</span><span class="signature">(unknown)</span>:
    </div>

        
            normalize() -> None
correct negative sizes


                            </div>
                            <div id="Rect.clip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.clip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">clip</span><span class="signature">(unknown)</span>:
    </div>

        
            clip(Rect) -> Rect
crops a rectangle inside another


                            </div>
                            <div id="Rect.clipline" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.clipline">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">clipline</span><span class="signature">(unknown)</span>:
    </div>

        
            clipline(x1, y1, x2, y2) -> ((cx1, cy1), (cx2, cy2))
clipline(x1, y1, x2, y2) -> ()
clipline((x1, y1), (x2, y2)) -> ((cx1, cy1), (cx2, cy2))
clipline((x1, y1), (x2, y2)) -> ()
clipline((x1, y1, x2, y2)) -> ((cx1, cy1), (cx2, cy2))
clipline((x1, y1, x2, y2)) -> ()
clipline(((x1, y1), (x2, y2))) -> ((cx1, cy1), (cx2, cy2))
clipline(((x1, y1), (x2, y2))) -> ()
crops a line inside a rectangle


                            </div>
                            <div id="Rect.clamp" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.clamp">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">clamp</span><span class="signature">(unknown)</span>:
    </div>

        
            clamp(Rect) -> Rect
moves the rectangle inside another


                            </div>
                            <div id="Rect.clamp_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.clamp_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">clamp_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            clamp_ip(Rect) -> None
moves the rectangle inside another, in place


                            </div>
                            <div id="Rect.copy" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.copy">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">copy</span><span class="signature">(unknown)</span>:
    </div>

        
            copy() -> Rect
copy the rectangle


                            </div>
                            <div id="Rect.fit" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.fit">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">fit</span><span class="signature">(unknown)</span>:
    </div>

        
            fit(Rect) -> Rect
resize and move a rectangle with aspect ratio


                            </div>
                            <div id="Rect.move" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.move">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">move</span><span class="signature">(unknown)</span>:
    </div>

        
            move(x, y) -> Rect
moves the rectangle


                            </div>
                            <div id="Rect.update" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.update">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">update</span><span class="signature">(unknown)</span>:
    </div>

        
            update(left, top, width, height) -> None
update((left, top), (width, height)) -> None
update(object) -> None
sets the position and size of the rectangle


                            </div>
                            <div id="Rect.inflate" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.inflate">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">inflate</span><span class="signature">(unknown)</span>:
    </div>

        
            inflate(x, y) -> Rect
grow or shrink the rectangle size


                            </div>
                            <div id="Rect.union" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.union">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">union</span><span class="signature">(unknown)</span>:
    </div>

        
            union(Rect) -> Rect
joins two rectangles into one


                            </div>
                            <div id="Rect.unionall" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.unionall">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">unionall</span><span class="signature">(unknown)</span>:
    </div>

        
            unionall(Rect_sequence) -> Rect
the union of many rectangles


                            </div>
                            <div id="Rect.move_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.move_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">move_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            move_ip(x, y) -> None
moves the rectangle, in place


                            </div>
                            <div id="Rect.inflate_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.inflate_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">inflate_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            inflate_ip(x, y) -> None
grow or shrink the rectangle size, in place


                            </div>
                            <div id="Rect.union_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.union_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">union_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            union_ip(Rect) -> None
joins two rectangles into one, in place


                            </div>
                            <div id="Rect.unionall_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.unionall_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">unionall_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            unionall_ip(Rect_sequence) -> None
the union of many rectangles, in place


                            </div>
                            <div id="Rect.collidepoint" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.collidepoint">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">collidepoint</span><span class="signature">(unknown)</span>:
    </div>

        
            collidepoint(x, y) -> bool
collidepoint((x,y)) -> bool
test if a point is inside a rectangle


                            </div>
                            <div id="Rect.colliderect" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.colliderect">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">colliderect</span><span class="signature">(unknown)</span>:
    </div>

        
            colliderect(Rect) -> bool
test if two rectangles overlap


                            </div>
                            <div id="Rect.collidelist" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.collidelist">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">collidelist</span><span class="signature">(unknown)</span>:
    </div>

        
            collidelist(list) -> index
test if one rectangle in a list intersects


                            </div>
                            <div id="Rect.collidelistall" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.collidelistall">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">collidelistall</span><span class="signature">(unknown)</span>:
    </div>

        
            collidelistall(list) -> indices
test if all rectangles in a list intersect


                            </div>
                            <div id="Rect.collidedict" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.collidedict">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">collidedict</span><span class="signature">(unknown)</span>:
    </div>

        
            collidedict(dict) -> (key, value)
collidedict(dict) -> None
collidedict(dict, use_values=0) -> (key, value)
collidedict(dict, use_values=0) -> None
test if one rectangle in a dictionary intersects


                            </div>
                            <div id="Rect.collidedictall" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.collidedictall">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">collidedictall</span><span class="signature">(unknown)</span>:
    </div>

        
            collidedictall(dict) -> [(key, value), ...]
collidedictall(dict, use_values=0) -> [(key, value), ...]
test if all rectangles in a dictionary intersect


                            </div>
                            <div id="Rect.contains" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Rect.contains">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">contains</span><span class="signature">(unknown)</span>:
    </div>

        
            contains(Rect) -> bool
test if one rectangle is inside another


                            </div>
                            <div id="Rect.x" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.x">#&nbsp;&nbsp</a>

        <span class="name">x</span>
    </div>

    

                            </div>
                            <div id="Rect.y" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.y">#&nbsp;&nbsp</a>

        <span class="name">y</span>
    </div>

    

                            </div>
                            <div id="Rect.w" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.w">#&nbsp;&nbsp</a>

        <span class="name">w</span>
    </div>

    

                            </div>
                            <div id="Rect.h" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.h">#&nbsp;&nbsp</a>

        <span class="name">h</span>
    </div>

    

                            </div>
                            <div id="Rect.width" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.width">#&nbsp;&nbsp</a>

        <span class="name">width</span>
    </div>

    

                            </div>
                            <div id="Rect.height" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.height">#&nbsp;&nbsp</a>

        <span class="name">height</span>
    </div>

    

                            </div>
                            <div id="Rect.top" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.top">#&nbsp;&nbsp</a>

        <span class="name">top</span>
    </div>

    

                            </div>
                            <div id="Rect.left" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.left">#&nbsp;&nbsp</a>

        <span class="name">left</span>
    </div>

    

                            </div>
                            <div id="Rect.bottom" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.bottom">#&nbsp;&nbsp</a>

        <span class="name">bottom</span>
    </div>

    

                            </div>
                            <div id="Rect.right" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.right">#&nbsp;&nbsp</a>

        <span class="name">right</span>
    </div>

    

                            </div>
                            <div id="Rect.centerx" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.centerx">#&nbsp;&nbsp</a>

        <span class="name">centerx</span>
    </div>

    

                            </div>
                            <div id="Rect.centery" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.centery">#&nbsp;&nbsp</a>

        <span class="name">centery</span>
    </div>

    

                            </div>
                            <div id="Rect.topleft" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.topleft">#&nbsp;&nbsp</a>

        <span class="name">topleft</span>
    </div>

    

                            </div>
                            <div id="Rect.topright" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.topright">#&nbsp;&nbsp</a>

        <span class="name">topright</span>
    </div>

    

                            </div>
                            <div id="Rect.bottomleft" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.bottomleft">#&nbsp;&nbsp</a>

        <span class="name">bottomleft</span>
    </div>

    

                            </div>
                            <div id="Rect.bottomright" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.bottomright">#&nbsp;&nbsp</a>

        <span class="name">bottomright</span>
    </div>

    

                            </div>
                            <div id="Rect.midtop" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.midtop">#&nbsp;&nbsp</a>

        <span class="name">midtop</span>
    </div>

    

                            </div>
                            <div id="Rect.midleft" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.midleft">#&nbsp;&nbsp</a>

        <span class="name">midleft</span>
    </div>

    

                            </div>
                            <div id="Rect.midbottom" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.midbottom">#&nbsp;&nbsp</a>

        <span class="name">midbottom</span>
    </div>

    

                            </div>
                            <div id="Rect.midright" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.midright">#&nbsp;&nbsp</a>

        <span class="name">midright</span>
    </div>

    

                            </div>
                            <div id="Rect.size" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.size">#&nbsp;&nbsp</a>

        <span class="name">size</span>
    </div>

    

                            </div>
                            <div id="Rect.center" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Rect.center">#&nbsp;&nbsp</a>

        <span class="name">center</span>
    </div>

    

                            </div>
                </section>
                <section id="Surface">
                                <div class="attr class">
        <a class="headerlink" href="#Surface">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">Surface</span>:
    </div>

        
            Surface((width, height), flags=0, depth=0, masks=None) -> Surface
Surface((width, height), flags=0, Surface) -> Surface
pygame object for representing images


                            <div id="Surface.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">Surface</span><span class="signature">(*args, **kwargs)</span>
    </div>

        
    

                            </div>
                            <div id="Surface.get_at" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_at">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_at</span><span class="signature">(unknown)</span>:
    </div>

        
            get_at((x, y)) -> Color
get the color value at a single pixel


                            </div>
                            <div id="Surface.set_at" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.set_at">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">set_at</span><span class="signature">(unknown)</span>:
    </div>

        
            set_at((x, y), Color) -> None
set the color value for a single pixel


                            </div>
                            <div id="Surface.get_at_mapped" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_at_mapped">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_at_mapped</span><span class="signature">(unknown)</span>:
    </div>

        
            get_at_mapped((x, y)) -> Color
get the mapped color value at a single pixel


                            </div>
                            <div id="Surface.map_rgb" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.map_rgb">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">map_rgb</span><span class="signature">(unknown)</span>:
    </div>

        
            map_rgb(Color) -> mapped_int
convert a color into a mapped color value


                            </div>
                            <div id="Surface.unmap_rgb" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.unmap_rgb">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">unmap_rgb</span><span class="signature">(unknown)</span>:
    </div>

        
            unmap_rgb(mapped_int) -> Color
convert a mapped integer color value into a Color


                            </div>
                            <div id="Surface.get_palette" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_palette">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_palette</span><span class="signature">(unknown)</span>:
    </div>

        
            get_palette() -> [RGB, RGB, RGB, ...]
get the color index palette for an 8-bit Surface


                            </div>
                            <div id="Surface.get_palette_at" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_palette_at">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_palette_at</span><span class="signature">(unknown)</span>:
    </div>

        
            get_palette_at(index) -> RGB
get the color for a single entry in a palette


                            </div>
                            <div id="Surface.set_palette" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.set_palette">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">set_palette</span><span class="signature">(unknown)</span>:
    </div>

        
            set_palette([RGB, RGB, RGB, ...]) -> None
set the color palette for an 8-bit Surface


                            </div>
                            <div id="Surface.set_palette_at" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.set_palette_at">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">set_palette_at</span><span class="signature">(unknown)</span>:
    </div>

        
            set_palette_at(index, RGB) -> None
set the color for a single index in an 8-bit Surface palette


                            </div>
                            <div id="Surface.lock" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.lock">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">lock</span><span class="signature">(unknown)</span>:
    </div>

        
            lock() -> None
lock the Surface memory for pixel access


                            </div>
                            <div id="Surface.unlock" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.unlock">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">unlock</span><span class="signature">(unknown)</span>:
    </div>

        
            unlock() -> None
unlock the Surface memory from pixel access


                            </div>
                            <div id="Surface.mustlock" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.mustlock">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">mustlock</span><span class="signature">(unknown)</span>:
    </div>

        
            mustlock() -> bool
test if the Surface requires locking


                            </div>
                            <div id="Surface.get_locked" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_locked">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_locked</span><span class="signature">(unknown)</span>:
    </div>

        
            get_locked() -> bool
test if the Surface is current locked


                            </div>
                            <div id="Surface.get_locks" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_locks">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_locks</span><span class="signature">(unknown)</span>:
    </div>

        
            get_locks() -> tuple
Gets the locks for the Surface


                            </div>
                            <div id="Surface.set_colorkey" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.set_colorkey">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">set_colorkey</span><span class="signature">(unknown)</span>:
    </div>

        
            set_colorkey(Color, flags=0) -> None
set_colorkey(None) -> None
Set the transparent colorkey


                            </div>
                            <div id="Surface.get_colorkey" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_colorkey">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_colorkey</span><span class="signature">(unknown)</span>:
    </div>

        
            get_colorkey() -> RGB or None
Get the current transparent colorkey


                            </div>
                            <div id="Surface.set_alpha" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.set_alpha">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">set_alpha</span><span class="signature">(unknown)</span>:
    </div>

        
            set_alpha(value, flags=0) -> None
set_alpha(None) -> None
set the alpha value for the full Surface image


                            </div>
                            <div id="Surface.get_alpha" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_alpha">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_alpha</span><span class="signature">(unknown)</span>:
    </div>

        
            get_alpha() -> int_value
get the current Surface transparency value


                            </div>
                            <div id="Surface.get_blendmode" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_blendmode">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_blendmode</span><span class="signature">(unknown)</span>:
    </div>

        
            Return the surface's SDL 2 blend mode


                            </div>
                            <div id="Surface.copy" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.copy">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">copy</span><span class="signature">(unknown)</span>:
    </div>

        
            copy() -> Surface
create a new copy of a Surface


                            </div>
                            <div id="Surface.convert" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.convert">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">convert</span><span class="signature">(unknown)</span>:
    </div>

        
            convert(Surface=None) -> Surface
convert(depth, flags=0) -> Surface
convert(masks, flags=0) -> Surface
change the pixel format of an image


                            </div>
                            <div id="Surface.convert_alpha" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.convert_alpha">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">convert_alpha</span><span class="signature">(unknown)</span>:
    </div>

        
            convert_alpha(Surface) -> Surface
convert_alpha() -> Surface
change the pixel format of an image including per pixel alphas


                            </div>
                            <div id="Surface.set_clip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.set_clip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">set_clip</span><span class="signature">(unknown)</span>:
    </div>

        
            set_clip(rect) -> None
set_clip(None) -> None
set the current clipping area of the Surface


                            </div>
                            <div id="Surface.get_clip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_clip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_clip</span><span class="signature">(unknown)</span>:
    </div>

        
            get_clip() -> Rect
get the current clipping area of the Surface


                            </div>
                            <div id="Surface.fill" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.fill">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">fill</span><span class="signature">(unknown)</span>:
    </div>

        
            fill(color, rect=None, special_flags=0) -> Rect
fill Surface with a solid color


                            </div>
                            <div id="Surface.blit" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.blit">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">blit</span><span class="signature">(unknown)</span>:
    </div>

        
            blit(source, dest, area=None, special_flags=0) -> Rect
draw one image onto another


                            </div>
                            <div id="Surface.blits" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.blits">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">blits</span><span class="signature">(unknown)</span>:
    </div>

        
            blits(blit_sequence=((source, dest), ...), doreturn=1) -> [Rect, ...] or None
blits(((source, dest, area), ...)) -> [Rect, ...]
blits(((source, dest, area, special_flags), ...)) -> [Rect, ...]
draw many images onto another


                            </div>
                            <div id="Surface.scroll" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.scroll">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">scroll</span><span class="signature">(unknown)</span>:
    </div>

        
            scroll(dx=0, dy=0) -> None
Shift the surface image in place


                            </div>
                            <div id="Surface.get_flags" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_flags">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_flags</span><span class="signature">(unknown)</span>:
    </div>

        
            get_flags() -> int
get the additional flags used for the Surface


                            </div>
                            <div id="Surface.get_size" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_size">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_size</span><span class="signature">(unknown)</span>:
    </div>

        
            get_size() -> (width, height)
get the dimensions of the Surface


                            </div>
                            <div id="Surface.get_width" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_width">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_width</span><span class="signature">(unknown)</span>:
    </div>

        
            get_width() -> width
get the width of the Surface


                            </div>
                            <div id="Surface.get_height" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_height">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_height</span><span class="signature">(unknown)</span>:
    </div>

        
            get_height() -> height
get the height of the Surface


                            </div>
                            <div id="Surface.get_rect" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_rect">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_rect</span><span class="signature">(unknown)</span>:
    </div>

        
            get_rect(**kwargs) -> Rect
get the rectangular area of the Surface


                            </div>
                            <div id="Surface.get_pitch" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_pitch">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_pitch</span><span class="signature">(unknown)</span>:
    </div>

        
            get_pitch() -> int
get the number of bytes used per Surface row


                            </div>
                            <div id="Surface.get_bitsize" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_bitsize">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_bitsize</span><span class="signature">(unknown)</span>:
    </div>

        
            get_bitsize() -> int
get the bit depth of the Surface pixel format


                            </div>
                            <div id="Surface.get_bytesize" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_bytesize">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_bytesize</span><span class="signature">(unknown)</span>:
    </div>

        
            get_bytesize() -> int
get the bytes used per Surface pixel


                            </div>
                            <div id="Surface.get_masks" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_masks">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_masks</span><span class="signature">(unknown)</span>:
    </div>

        
            get_masks() -> (R, G, B, A)
the bitmasks needed to convert between a color and a mapped integer


                            </div>
                            <div id="Surface.get_shifts" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_shifts">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_shifts</span><span class="signature">(unknown)</span>:
    </div>

        
            get_shifts() -> (R, G, B, A)
the bit shifts needed to convert between a color and a mapped integer


                            </div>
                            <div id="Surface.set_masks" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.set_masks">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">set_masks</span><span class="signature">(unknown)</span>:
    </div>

        
            set_masks((r,g,b,a)) -> None
set the bitmasks needed to convert between a color and a mapped integer


                            </div>
                            <div id="Surface.set_shifts" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.set_shifts">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">set_shifts</span><span class="signature">(unknown)</span>:
    </div>

        
            set_shifts((r,g,b,a)) -> None
sets the bit shifts needed to convert between a color and a mapped integer


                            </div>
                            <div id="Surface.get_losses" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_losses">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_losses</span><span class="signature">(unknown)</span>:
    </div>

        
            get_losses() -> (R, G, B, A)
the significant bits used to convert between a color and a mapped integer


                            </div>
                            <div id="Surface.subsurface" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.subsurface">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">subsurface</span><span class="signature">(unknown)</span>:
    </div>

        
            subsurface(Rect) -> Surface
create a new surface that references its parent


                            </div>
                            <div id="Surface.get_offset" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_offset">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_offset</span><span class="signature">(unknown)</span>:
    </div>

        
            get_offset() -> (x, y)
find the position of a child subsurface inside a parent


                            </div>
                            <div id="Surface.get_abs_offset" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_abs_offset">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_abs_offset</span><span class="signature">(unknown)</span>:
    </div>

        
            get_abs_offset() -> (x, y)
find the absolute position of a child subsurface inside its top level parent


                            </div>
                            <div id="Surface.get_parent" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_parent">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_parent</span><span class="signature">(unknown)</span>:
    </div>

        
            get_parent() -> Surface
find the parent of a subsurface


                            </div>
                            <div id="Surface.get_abs_parent" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_abs_parent">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_abs_parent</span><span class="signature">(unknown)</span>:
    </div>

        
            get_abs_parent() -> Surface
find the top level parent of a subsurface


                            </div>
                            <div id="Surface.get_bounding_rect" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_bounding_rect">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_bounding_rect</span><span class="signature">(unknown)</span>:
    </div>

        
            get_bounding_rect(min_alpha = 1) -> Rect
find the smallest rect containing data


                            </div>
                            <div id="Surface.get_view" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_view">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_view</span><span class="signature">(unknown)</span>:
    </div>

        
            get_view(<kind>='2') -> BufferProxy
return a buffer view of the Surface's pixels.


                            </div>
                            <div id="Surface.get_buffer" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Surface.get_buffer">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">get_buffer</span><span class="signature">(unknown)</span>:
    </div>

        
            get_buffer() -> BufferProxy
acquires a buffer object for the pixels of the Surface.


                            </div>
                </section>
                <section id="Color">
                                <div class="attr class">
        <a class="headerlink" href="#Color">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">Color</span>:
    </div>

        
            Color(r, g, b) -> Color
Color(r, g, b, a=255) -> Color
Color(color_value) -> Color
pygame object for color representations


                            <div id="Color.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Color.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">Color</span><span class="signature">(*args, **kwargs)</span>
    </div>

        
    

                            </div>
                            <div id="Color.normalize" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Color.normalize">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">normalize</span><span class="signature">(unknown)</span>:
    </div>

        
            normalize() -> tuple
Returns the normalized RGBA values of the Color.


                            </div>
                            <div id="Color.correct_gamma" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Color.correct_gamma">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">correct_gamma</span><span class="signature">(unknown)</span>:
    </div>

        
            correct_gamma (gamma) -> Color
Applies a certain gamma value to the Color.


                            </div>
                            <div id="Color.set_length" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Color.set_length">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">set_length</span><span class="signature">(unknown)</span>:
    </div>

        
            set_length(len) -> None
Set the number of elements in the Color to 1,2,3, or 4.


                            </div>
                            <div id="Color.lerp" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Color.lerp">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">lerp</span><span class="signature">(unknown)</span>:
    </div>

        
            lerp(Color, float) -> Color
returns a linear interpolation to the given Color.


                            </div>
                            <div id="Color.premul_alpha" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Color.premul_alpha">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">premul_alpha</span><span class="signature">(unknown)</span>:
    </div>

        
            premul_alpha() -> Color
returns a Color where the r,g,b components have been multiplied by the alpha.


                            </div>
                            <div id="Color.update" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Color.update">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">update</span><span class="signature">(unknown)</span>:
    </div>

        
            update(r, g, b) -> None
update(r, g, b, a=255) -> None
update(color_value) -> None
Sets the elements of the color


                            </div>
                            <div id="Color.r" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Color.r">#&nbsp;&nbsp</a>

        <span class="name">r</span>
    </div>

            r -> int
Gets or sets the red value of the Color.


                            </div>
                            <div id="Color.g" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Color.g">#&nbsp;&nbsp</a>

        <span class="name">g</span>
    </div>

            g -> int
Gets or sets the green value of the Color.


                            </div>
                            <div id="Color.b" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Color.b">#&nbsp;&nbsp</a>

        <span class="name">b</span>
    </div>

            b -> int
Gets or sets the blue value of the Color.


                            </div>
                            <div id="Color.a" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Color.a">#&nbsp;&nbsp</a>

        <span class="name">a</span>
    </div>

            a -> int
Gets or sets the alpha value of the Color.


                            </div>
                            <div id="Color.hsva" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Color.hsva">#&nbsp;&nbsp</a>

        <span class="name">hsva</span>
    </div>

            hsva -> tuple
Gets or sets the HSVA representation of the Color.


                            </div>
                            <div id="Color.hsla" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Color.hsla">#&nbsp;&nbsp</a>

        <span class="name">hsla</span>
    </div>

            hsla -> tuple
Gets or sets the HSLA representation of the Color.


                            </div>
                            <div id="Color.i1i2i3" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Color.i1i2i3">#&nbsp;&nbsp</a>

        <span class="name">i1i2i3</span>
    </div>

            i1i2i3 -> tuple
Gets or sets the I1I2I3 representation of the Color.


                            </div>
                            <div id="Color.cmy" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Color.cmy">#&nbsp;&nbsp</a>

        <span class="name">cmy</span>
    </div>

            cmy -> tuple
Gets or sets the CMY representation of the Color.


                            </div>
                </section>
                <section id="PixelArray">
                                <div class="attr class">
        <a class="headerlink" href="#PixelArray">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">PixelArray</span>:
    </div>

        
            PixelArray(Surface) -> PixelArray
pygame object for direct pixel access of surfaces


                            <div id="PixelArray.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#PixelArray.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">PixelArray</span><span class="signature">()</span>
    </div>

        
    

                            </div>
                            <div id="PixelArray.compare" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#PixelArray.compare">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">compare</span><span class="signature">(unknown)</span>:
    </div>

        
            compare(array, distance=0, weights=(0.299, 0.587, 0.114)) -> PixelArray
Compares the PixelArray with another one.


                            </div>
                            <div id="PixelArray.extract" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#PixelArray.extract">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">extract</span><span class="signature">(unknown)</span>:
    </div>

        
            extract(color, distance=0, weights=(0.299, 0.587, 0.114)) -> PixelArray
Extracts the passed color from the PixelArray.


                            </div>
                            <div id="PixelArray.make_surface" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#PixelArray.make_surface">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">make_surface</span><span class="signature">(unknown)</span>:
    </div>

        
            make_surface() -> Surface
Creates a new Surface from the current PixelArray.


                            </div>
                            <div id="PixelArray.close" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#PixelArray.close">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">close</span><span class="signature">(unknown)</span>:
    </div>

        
            transpose() -> PixelArray
Closes the PixelArray, and releases Surface lock.


                            </div>
                            <div id="PixelArray.replace" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#PixelArray.replace">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">replace</span><span class="signature">(unknown)</span>:
    </div>

        
            replace(color, repcolor, distance=0, weights=(0.299, 0.587, 0.114)) -> None
Replaces the passed color in the PixelArray with another one.


                            </div>
                            <div id="PixelArray.transpose" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#PixelArray.transpose">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">transpose</span><span class="signature">(unknown)</span>:
    </div>

        
            transpose() -> PixelArray
Exchanges the x and y axis.


                            </div>
                            <div id="PixelArray.surface" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#PixelArray.surface">#&nbsp;&nbsp</a>

        <span class="name">surface</span>
    </div>

            surface -> Surface
Gets the Surface the PixelArray uses.


                            </div>
                            <div id="PixelArray.itemsize" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#PixelArray.itemsize">#&nbsp;&nbsp</a>

        <span class="name">itemsize</span>
    </div>

            itemsize -> int
Returns the byte size of a pixel array item


                            </div>
                            <div id="PixelArray.shape" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#PixelArray.shape">#&nbsp;&nbsp</a>

        <span class="name">shape</span>
    </div>

            shape -> tuple of int's
Returns the array size.


                            </div>
                            <div id="PixelArray.strides" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#PixelArray.strides">#&nbsp;&nbsp</a>

        <span class="name">strides</span>
    </div>

            strides -> tuple of int's
Returns byte offsets for each array dimension.


                            </div>
                            <div id="PixelArray.ndim" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#PixelArray.ndim">#&nbsp;&nbsp</a>

        <span class="name">ndim</span>
    </div>

            ndim -> int
Returns the number of dimensions.


                            </div>
                </section>
                <section id="Vector2">
                                <div class="attr class">
        <a class="headerlink" href="#Vector2">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">Vector2</span>:
    </div>

        
            Vector2() -> Vector2
Vector2(int) -> Vector2
Vector2(float) -> Vector2
Vector2(Vector2) -> Vector2
Vector2(x, y) -> Vector2
Vector2((x, y)) -> Vector2
a 2-Dimensional Vector


                            <div id="Vector2.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">Vector2</span><span class="signature">(*args, **kwargs)</span>
    </div>

        
    

                            </div>
                            <div id="Vector2.length" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.length">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">length</span><span class="signature">(unknown)</span>:
    </div>

        
            length() -> float
returns the Euclidean length of the vector.


                            </div>
                            <div id="Vector2.length_squared" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.length_squared">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">length_squared</span><span class="signature">(unknown)</span>:
    </div>

        
            length_squared() -> float
returns the squared Euclidean length of the vector.


                            </div>
                            <div id="Vector2.magnitude" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.magnitude">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">magnitude</span><span class="signature">(unknown)</span>:
    </div>

        
            magnitude() -> float
returns the Euclidean magnitude of the vector.


                            </div>
                            <div id="Vector2.magnitude_squared" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.magnitude_squared">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">magnitude_squared</span><span class="signature">(unknown)</span>:
    </div>

        
            magnitude_squared() -> float
returns the squared magnitude of the vector.


                            </div>
                            <div id="Vector2.rotate" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.rotate">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate(angle) -> Vector2
rotates a vector by a given angle in degrees.


                            </div>
                            <div id="Vector2.rotate_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.rotate_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_ip(angle) -> None
rotates the vector by a given angle in degrees in place.


                            </div>
                            <div id="Vector2.rotate_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.rotate_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_rad(angle) -> Vector2
rotates a vector by a given angle in radians.


                            </div>
                            <div id="Vector2.rotate_ip_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.rotate_ip_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_ip_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_ip_rad(angle) -> None
rotates the vector by a given angle in radians in place.


                            </div>
                            <div id="Vector2.slerp" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.slerp">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">slerp</span><span class="signature">(unknown)</span>:
    </div>

        
            slerp(Vector2, float) -> Vector2
returns a spherical interpolation to the given vector.


                            </div>
                            <div id="Vector2.lerp" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.lerp">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">lerp</span><span class="signature">(unknown)</span>:
    </div>

        
            lerp(Vector2, float) -> Vector2
returns a linear interpolation to the given vector.


                            </div>
                            <div id="Vector2.normalize" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.normalize">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">normalize</span><span class="signature">(unknown)</span>:
    </div>

        
            normalize() -> Vector2
returns a vector with the same direction but length 1.


                            </div>
                            <div id="Vector2.normalize_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.normalize_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">normalize_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            normalize_ip() -> None
normalizes the vector in place so that its length is 1.


                            </div>
                            <div id="Vector2.is_normalized" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.is_normalized">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">is_normalized</span><span class="signature">(unknown)</span>:
    </div>

        
            is_normalized() -> Bool
tests if the vector is normalized i.e. has length == 1.


                            </div>
                            <div id="Vector2.cross" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.cross">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">cross</span><span class="signature">(unknown)</span>:
    </div>

        
            cross(Vector2) -> Vector2
calculates the cross- or vector-product


                            </div>
                            <div id="Vector2.dot" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.dot">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">dot</span><span class="signature">(unknown)</span>:
    </div>

        
            dot(Vector2) -> float
calculates the dot- or scalar-product with the other vector


                            </div>
                            <div id="Vector2.angle_to" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.angle_to">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">angle_to</span><span class="signature">(unknown)</span>:
    </div>

        
            angle_to(Vector2) -> float
calculates the angle to a given vector in degrees.


                            </div>
                            <div id="Vector2.update" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.update">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">update</span><span class="signature">(unknown)</span>:
    </div>

        
            update() -> None
update(int) -> None
update(float) -> None
update(Vector2) -> None
update(x, y) -> None
update((x, y)) -> None
Sets the coordinates of the vector.


                            </div>
                            <div id="Vector2.scale_to_length" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.scale_to_length">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">scale_to_length</span><span class="signature">(unknown)</span>:
    </div>

        
            scale_to_length(float) -> None
scales the vector to a given length.


                            </div>
                            <div id="Vector2.reflect" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.reflect">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">reflect</span><span class="signature">(unknown)</span>:
    </div>

        
            reflect(Vector2) -> Vector2
returns a vector reflected of a given normal.


                            </div>
                            <div id="Vector2.reflect_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.reflect_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">reflect_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            reflect_ip(Vector2) -> None
reflect the vector of a given normal in place.


                            </div>
                            <div id="Vector2.distance_to" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.distance_to">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">distance_to</span><span class="signature">(unknown)</span>:
    </div>

        
            distance_to(Vector2) -> float
calculates the Euclidean distance to a given vector.


                            </div>
                            <div id="Vector2.distance_squared_to" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.distance_squared_to">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">distance_squared_to</span><span class="signature">(unknown)</span>:
    </div>

        
            distance_squared_to(Vector2) -> float
calculates the squared Euclidean distance to a given vector.


                            </div>
                            <div id="Vector2.elementwise" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.elementwise">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">elementwise</span><span class="signature">(unknown)</span>:
    </div>

        
            elementwise() -> VectorElementwiseProxy
The next operation will be performed elementwise.


                            </div>
                            <div id="Vector2.as_polar" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.as_polar">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">as_polar</span><span class="signature">(unknown)</span>:
    </div>

        
            as_polar() -> (r, phi)
returns a tuple with radial distance and azimuthal angle.


                            </div>
                            <div id="Vector2.from_polar" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.from_polar">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">from_polar</span><span class="signature">(unknown)</span>:
    </div>

        
            from_polar((r, phi)) -> None
Sets x and y from a polar coordinates tuple.


                            </div>
                            <div id="Vector2.project" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector2.project">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">project</span><span class="signature">(unknown)</span>:
    </div>

        
            project(Vector2) -> Vector2
projects a vector onto another.


                            </div>
                            <div id="Vector2.epsilon" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Vector2.epsilon">#&nbsp;&nbsp</a>

        <span class="name">epsilon</span>
    </div>

            small value used in comparisons


                            </div>
                            <div id="Vector2.x" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Vector2.x">#&nbsp;&nbsp</a>

        <span class="name">x</span>
    </div>

    

                            </div>
                            <div id="Vector2.y" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Vector2.y">#&nbsp;&nbsp</a>

        <span class="name">y</span>
    </div>

    

                            </div>
                </section>
                <section id="Vector3">
                                <div class="attr class">
        <a class="headerlink" href="#Vector3">#&nbsp;&nbsp</a>

        
        <span class="def">class</span>
        <span class="name">Vector3</span>:
    </div>

        
            Vector3() -> Vector3
Vector3(int) -> Vector3
Vector3(float) -> Vector3
Vector3(Vector3) -> Vector3
Vector3(x, y, z) -> Vector3
Vector3((x, y, z)) -> Vector3
a 3-Dimensional Vector


                            <div id="Vector3.__init__" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.__init__">#&nbsp;&nbsp</a>

        
            <span class="name">Vector3</span><span class="signature">(*args, **kwargs)</span>
    </div>

        
    

                            </div>
                            <div id="Vector3.length" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.length">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">length</span><span class="signature">(unknown)</span>:
    </div>

        
            length() -> float
returns the Euclidean length of the vector.


                            </div>
                            <div id="Vector3.length_squared" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.length_squared">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">length_squared</span><span class="signature">(unknown)</span>:
    </div>

        
            length_squared() -> float
returns the squared Euclidean length of the vector.


                            </div>
                            <div id="Vector3.magnitude" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.magnitude">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">magnitude</span><span class="signature">(unknown)</span>:
    </div>

        
            magnitude() -> float
returns the Euclidean magnitude of the vector.


                            </div>
                            <div id="Vector3.magnitude_squared" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.magnitude_squared">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">magnitude_squared</span><span class="signature">(unknown)</span>:
    </div>

        
            magnitude_squared() -> float
returns the squared Euclidean magnitude of the vector.


                            </div>
                            <div id="Vector3.rotate" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate(angle, Vector3) -> Vector3
rotates a vector by a given angle in degrees.


                            </div>
                            <div id="Vector3.rotate_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_ip(angle, Vector3) -> None
rotates the vector by a given angle in degrees in place.


                            </div>
                            <div id="Vector3.rotate_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_rad(angle, Vector3) -> Vector3
rotates a vector by a given angle in radians.


                            </div>
                            <div id="Vector3.rotate_ip_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_ip_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_ip_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_ip_rad(angle, Vector3) -> None
rotates the vector by a given angle in radians in place.


                            </div>
                            <div id="Vector3.rotate_x" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_x">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_x</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_x(angle) -> Vector3
rotates a vector around the x-axis by the angle in degrees.


                            </div>
                            <div id="Vector3.rotate_x_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_x_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_x_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_x_ip(angle) -> None
rotates the vector around the x-axis by the angle in degrees in place.


                            </div>
                            <div id="Vector3.rotate_x_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_x_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_x_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_x_rad(angle) -> Vector3
rotates a vector around the x-axis by the angle in radians.


                            </div>
                            <div id="Vector3.rotate_x_ip_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_x_ip_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_x_ip_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_x_ip_rad(angle) -> None
rotates the vector around the x-axis by the angle in radians in place.


                            </div>
                            <div id="Vector3.rotate_y" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_y">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_y</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_y(angle) -> Vector3
rotates a vector around the y-axis by the angle in degrees.


                            </div>
                            <div id="Vector3.rotate_y_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_y_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_y_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_y_ip(angle) -> None
rotates the vector around the y-axis by the angle in degrees in place.


                            </div>
                            <div id="Vector3.rotate_y_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_y_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_y_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_y_rad(angle) -> Vector3
rotates a vector around the y-axis by the angle in radians.


                            </div>
                            <div id="Vector3.rotate_y_ip_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_y_ip_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_y_ip_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_y_ip_rad(angle) -> None
rotates the vector around the y-axis by the angle in radians in place.


                            </div>
                            <div id="Vector3.rotate_z" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_z">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_z</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_z(angle) -> Vector3
rotates a vector around the z-axis by the angle in degrees.


                            </div>
                            <div id="Vector3.rotate_z_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_z_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_z_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_z_ip(angle) -> None
rotates the vector around the z-axis by the angle in degrees in place.


                            </div>
                            <div id="Vector3.rotate_z_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_z_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_z_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_z_rad(angle) -> Vector3
rotates a vector around the z-axis by the angle in radians.


                            </div>
                            <div id="Vector3.rotate_z_ip_rad" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.rotate_z_ip_rad">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">rotate_z_ip_rad</span><span class="signature">(unknown)</span>:
    </div>

        
            rotate_z_ip_rad(angle) -> None
rotates the vector around the z-axis by the angle in radians in place.


                            </div>
                            <div id="Vector3.slerp" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.slerp">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">slerp</span><span class="signature">(unknown)</span>:
    </div>

        
            slerp(Vector3, float) -> Vector3
returns a spherical interpolation to the given vector.


                            </div>
                            <div id="Vector3.lerp" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.lerp">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">lerp</span><span class="signature">(unknown)</span>:
    </div>

        
            lerp(Vector3, float) -> Vector3
returns a linear interpolation to the given vector.


                            </div>
                            <div id="Vector3.normalize" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.normalize">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">normalize</span><span class="signature">(unknown)</span>:
    </div>

        
            normalize() -> Vector3
returns a vector with the same direction but length 1.


                            </div>
                            <div id="Vector3.normalize_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.normalize_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">normalize_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            normalize_ip() -> None
normalizes the vector in place so that its length is 1.


                            </div>
                            <div id="Vector3.is_normalized" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.is_normalized">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">is_normalized</span><span class="signature">(unknown)</span>:
    </div>

        
            is_normalized() -> Bool
tests if the vector is normalized i.e. has length == 1.


                            </div>
                            <div id="Vector3.cross" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.cross">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">cross</span><span class="signature">(unknown)</span>:
    </div>

        
            cross(Vector3) -> Vector3
calculates the cross- or vector-product


                            </div>
                            <div id="Vector3.dot" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.dot">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">dot</span><span class="signature">(unknown)</span>:
    </div>

        
            dot(Vector3) -> float
calculates the dot- or scalar-product with the other vector


                            </div>
                            <div id="Vector3.angle_to" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.angle_to">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">angle_to</span><span class="signature">(unknown)</span>:
    </div>

        
            angle_to(Vector3) -> float
calculates the angle to a given vector in degrees.


                            </div>
                            <div id="Vector3.update" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.update">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">update</span><span class="signature">(unknown)</span>:
    </div>

        
            update() -> None
update(int) -> None
update(float) -> None
update(Vector3) -> None
update(x, y, z) -> None
update((x, y, z)) -> None
Sets the coordinates of the vector.


                            </div>
                            <div id="Vector3.scale_to_length" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.scale_to_length">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">scale_to_length</span><span class="signature">(unknown)</span>:
    </div>

        
            scale_to_length(float) -> None
scales the vector to a given length.


                            </div>
                            <div id="Vector3.reflect" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.reflect">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">reflect</span><span class="signature">(unknown)</span>:
    </div>

        
            reflect(Vector3) -> Vector3
returns a vector reflected of a given normal.


                            </div>
                            <div id="Vector3.reflect_ip" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.reflect_ip">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">reflect_ip</span><span class="signature">(unknown)</span>:
    </div>

        
            reflect_ip(Vector3) -> None
reflect the vector of a given normal in place.


                            </div>
                            <div id="Vector3.distance_to" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.distance_to">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">distance_to</span><span class="signature">(unknown)</span>:
    </div>

        
            distance_to(Vector3) -> float
calculates the Euclidean distance to a given vector.


                            </div>
                            <div id="Vector3.distance_squared_to" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.distance_squared_to">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">distance_squared_to</span><span class="signature">(unknown)</span>:
    </div>

        
            distance_squared_to(Vector3) -> float
calculates the squared Euclidean distance to a given vector.


                            </div>
                            <div id="Vector3.elementwise" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.elementwise">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">elementwise</span><span class="signature">(unknown)</span>:
    </div>

        
            elementwise() -> VectorElementwiseProxy
The next operation will be performed elementwise.


                            </div>
                            <div id="Vector3.as_spherical" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.as_spherical">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">as_spherical</span><span class="signature">(unknown)</span>:
    </div>

        
            as_spherical() -> (r, theta, phi)
returns a tuple with radial distance, inclination and azimuthal angle.


                            </div>
                            <div id="Vector3.from_spherical" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.from_spherical">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">from_spherical</span><span class="signature">(unknown)</span>:
    </div>

        
            from_spherical((r, theta, phi)) -> None
Sets x, y and z from a spherical coordinates 3-tuple.


                            </div>
                            <div id="Vector3.project" class="classattr">
                                        <div class="attr function"><a class="headerlink" href="#Vector3.project">#&nbsp;&nbsp</a>

        
            <span class="def">def</span>
            <span class="name">project</span><span class="signature">(unknown)</span>:
    </div>

        
            project(Vector3) -> Vector3
projects a vector onto another.


                            </div>
                            <div id="Vector3.epsilon" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Vector3.epsilon">#&nbsp;&nbsp</a>

        <span class="name">epsilon</span>
    </div>

            small value used in comparisons


                            </div>
                            <div id="Vector3.x" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Vector3.x">#&nbsp;&nbsp</a>

        <span class="name">x</span>
    </div>

    

                            </div>
                            <div id="Vector3.y" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Vector3.y">#&nbsp;&nbsp</a>

        <span class="name">y</span>
    </div>

    

                            </div>
                            <div id="Vector3.z" class="classattr">
                                            <div class="attr variable"><a class="headerlink" href="#Vector3.z">#&nbsp;&nbsp</a>

        <span class="name">z</span>
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