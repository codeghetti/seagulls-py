## [seagulls](../seagulls).engine
Core Engine Components

??? note "View Source"
    ```python
        """Core Engine Components"""
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
            "flag_from_string",
            "CollidableObject",
            "IGameScene",
            "IProvideGameScenes",
            "IProvideGameSessions",
            "IGameSession",
            "SurfaceRenderer",
            "GameClock",
            "GameControls",
            "GameObject",
            "GameObjectsCollection",
            "GameSettings",
            "Rect",
            "Surface",
            "Color",
            "PixelArray",
            "Vector2",
            "Vector3",
        ]

    ```

### flag_from_string

##### def flag_from_string(value: str) -&gt; int:

??? note "View Source"
    ```python
        def flag_from_string(value: str) -> int:
            if not isinstance(value, str):
                raise ValueError(f"Value must be a string of 0s and 1s: {value}")

            return int(value, 2)

    ```



### CollidableObject
@dataclass(frozen=True)

#### class `CollidableObject` :

??? note "View Source"
    ```python
        @dataclass(frozen=True)
        class CollidableObject:
            layer: int
            mask: int

            def filter_by_mask(
                    self, targets: Tuple["CollidableObject", ...]) -> Tuple["CollidableObject", ...]:
                result = []
                for t in targets:
                    if self.is_in_mask(t):
                        result.append(t)

                return tuple(result)

            def is_in_mask(self, target: "CollidableObject") -> bool:
                logger.debug(f"targeting items located in mask: {self.mask:b}")
                logger.debug(f"target is located in layer: {target.layer:b}")
                logger.debug(f"& result: {self.mask & target.layer:b}")
                return self.mask & target.layer > 0

            def __repr__(self) -> str:
                return f"{self.__class__.__name__}(layer={self.layer:b}, mask={self.mask:b})"

    ```

CollidableObject(layer: int, mask: int)



##### CollidableObject(layer: int, mask: int):





##### def filter_by_mask(
    self,
    targets: Tuple[seagulls.engine._collisions.CollidableObject, ...]
) -&gt; Tuple[seagulls.engine._collisions.CollidableObject, ...]:

??? note "View Source"
    ```python
            def filter_by_mask(
                    self, targets: Tuple["CollidableObject", ...]) -> Tuple["CollidableObject", ...]:
                result = []
                for t in targets:
                    if self.is_in_mask(t):
                        result.append(t)

                return tuple(result)

    ```




##### def is_in_mask(self, target: seagulls.engine._collisions.CollidableObject) -&gt; bool:

??? note "View Source"
    ```python
            def is_in_mask(self, target: "CollidableObject") -> bool:
                logger.debug(f"targeting items located in mask: {self.mask:b}")
                logger.debug(f"target is located in layer: {target.layer:b}")
                logger.debug(f"& result: {self.mask & target.layer:b}")
                return self.mask & target.layer > 0

    ```



### IGameScene

#### class `IGameScene` (abc.ABC):

??? note "View Source"
    ```python
        class IGameScene(ABC):
            """
            This class is for X and Y.
            """

            @abstractmethod
            def start(self) -> None:
                pass

            @abstractmethod
            def should_quit(self) -> bool:
                pass

            @abstractmethod
            def tick(self) -> None:
                pass

    ```

This class is for X and Y.


@abstractmethod

##### def start(self) -&gt; None:

??? note "View Source"
    ```python
            @abstractmethod
            def start(self) -> None:
                pass

    ```



@abstractmethod

##### def should_quit(self) -&gt; bool:

??? note "View Source"
    ```python
            @abstractmethod
            def should_quit(self) -> bool:
                pass

    ```



@abstractmethod

##### def tick(self) -&gt; None:

??? note "View Source"
    ```python
            @abstractmethod
            def tick(self) -> None:
                pass

    ```



### IProvideGameScenes

#### class `IProvideGameScenes` (abc.ABC):

??? note "View Source"
    ```python
        class IProvideGameScenes(ABC):

            @abstractmethod
            def get_scene(self) -> IGameScene:
                pass

    ```

Helper class that provides a standard way to create an ABC using
inheritance.


@abstractmethod

##### def get_scene(self) -&gt; seagulls.engine._game_scene.IGameScene:

??? note "View Source"
    ```python
            @abstractmethod
            def get_scene(self) -> IGameScene:
                pass

    ```



### IProvideGameSessions

#### class `IProvideGameSessions` (abc.ABC):

??? note "View Source"
    ```python
        class IProvideGameSessions(ABC):

            @abstractmethod
            def get_session(self, scene: str) -> IGameSession:
                pass

    ```

Helper class that provides a standard way to create an ABC using
inheritance.


@abstractmethod

##### def get_session(self, scene: str) -&gt; seagulls.engine._game_session.IGameSession:

??? note "View Source"
    ```python
            @abstractmethod
            def get_session(self, scene: str) -> IGameSession:
                pass

    ```



### IGameSession

#### class `IGameSession` (abc.ABC):

??? note "View Source"
    ```python
        class IGameSession(ABC):

            @abstractmethod
            def start(self) -> None:
                pass

            @abstractmethod
            def wait_for_completion(self) -> None:
                pass

            @abstractmethod
            def stop(self) -> None:
                pass

    ```

Helper class that provides a standard way to create an ABC using
inheritance.


@abstractmethod

##### def start(self) -&gt; None:

??? note "View Source"
    ```python
            @abstractmethod
            def start(self) -> None:
                pass

    ```



@abstractmethod

##### def wait_for_completion(self) -&gt; None:

??? note "View Source"
    ```python
            @abstractmethod
            def wait_for_completion(self) -> None:
                pass

    ```



@abstractmethod

##### def stop(self) -&gt; None:

??? note "View Source"
    ```python
            @abstractmethod
            def stop(self) -> None:
                pass

    ```



### SurfaceRenderer

#### class `SurfaceRenderer` :

??? note "View Source"
    ```python
        class SurfaceRenderer:
            def start(self) -> None:
                self._get_surface()

            def render(self, surface: Surface) -> None:
                self._get_surface().blit(surface, (0, 0))
                pygame.display.flip()

            @lru_cache()
            def _get_surface(self) -> Surface:
                return pygame.display.set_mode((1024, 600))

    ```




##### SurfaceRenderer():





##### def start(self) -&gt; None:

??? note "View Source"
    ```python
            def start(self) -> None:
                self._get_surface()

    ```




##### def render(self, surface: pygame.Surface) -&gt; None:

??? note "View Source"
    ```python
            def render(self, surface: Surface) -> None:
                self._get_surface().blit(surface, (0, 0))
                pygame.display.flip()

    ```



### GameClock

#### class `GameClock` (seagulls.engine._game_object.GameObject):

??? note "View Source"
    ```python
        class GameClock(GameObject):
            _clock: Clock
            _ticks: int
            _delta: int

            def __init__(self):
                self._clock = Clock()
                self._ticks = 0
                self._delta = 0

            def tick(self) -> None:
                self._delta = self._clock.tick()

            def render(self, surface: Surface) -> None:
                pass

            def get_time(self) -> int:
                return self._delta

            def get_fps(self) -> float:
                return self._clock.get_fps()

    ```

Interface for anything representing an object in the scene.



##### GameClock():

??? note "View Source"
    ```python
            def __init__(self):
                self._clock = Clock()
                self._ticks = 0
                self._delta = 0

    ```




##### def tick(self) -&gt; None:

??? note "View Source"
    ```python
            def tick(self) -> None:
                self._delta = self._clock.tick()

    ```




##### def render(self, surface: pygame.Surface) -&gt; None:

??? note "View Source"
    ```python
            def render(self, surface: Surface) -> None:
                pass

    ```




##### def get_time(self) -&gt; int:

??? note "View Source"
    ```python
            def get_time(self) -> int:
                return self._delta

    ```




##### def get_fps(self) -&gt; float:

??? note "View Source"
    ```python
            def get_fps(self) -> float:
                return self._clock.get_fps()

    ```



### GameControls

#### class `GameControls` (seagulls.engine._game_object.GameObject):

??? note "View Source"
    ```python
        class GameControls(GameObject):

            _events: List[Event]

            def __init__(self):
                self._events = []

            def tick(self):
                self._events = pygame.event.get()

            def should_quit(self) -> bool:
                for event in self._events:
                    if event.type == pygame.QUIT:
                        return True

                    if self._is_key_down_event(event, pygame.K_ESCAPE):
                        return True

                return False

            def should_fire(self) -> bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_SPACE):
                        return True

                return False

            def is_left_moving(self) -> bool:
                return pygame.key.get_pressed()[pygame.K_LEFT]

            def is_right_moving(self) -> bool:
                return pygame.key.get_pressed()[pygame.K_RIGHT]

            def should_toggle_debug_hud(self) -> bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_BACKQUOTE):
                        return True

                return False

            def is_click_initialized(self) -> bool:
                for event in self._events:
                    if not event.type == pygame.MOUSEBUTTONDOWN:
                        continue

                    return pygame.mouse.get_pressed(num_buttons=3)[0]

                return False

            def is_mouse_down(self) -> bool:
                return pygame.mouse.get_pressed(num_buttons=3)[0]

            def _is_key_down_event(self, event: Event, key: int) -> bool:
                return event.type == pygame.KEYDOWN and event.key == key

            def _is_key_up_event(self, event: Event, key: int) -> bool:
                return event.type == pygame.KEYUP and event.key == key

            def render(self, surface: pygame.Surface) -> None:
                pass

    ```

Interface for anything representing an object in the scene.



##### GameControls():

??? note "View Source"
    ```python
            def __init__(self):
                self._events = []

    ```




##### def tick(self):

??? note "View Source"
    ```python
            def tick(self):
                self._events = pygame.event.get()

    ```




##### def should_quit(self) -&gt; bool:

??? note "View Source"
    ```python
            def should_quit(self) -> bool:
                for event in self._events:
                    if event.type == pygame.QUIT:
                        return True

                    if self._is_key_down_event(event, pygame.K_ESCAPE):
                        return True

                return False

    ```




##### def should_fire(self) -&gt; bool:

??? note "View Source"
    ```python
            def should_fire(self) -> bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_SPACE):
                        return True

                return False

    ```




##### def is_left_moving(self) -&gt; bool:

??? note "View Source"
    ```python
            def is_left_moving(self) -> bool:
                return pygame.key.get_pressed()[pygame.K_LEFT]

    ```




##### def is_right_moving(self) -&gt; bool:

??? note "View Source"
    ```python
            def is_right_moving(self) -> bool:
                return pygame.key.get_pressed()[pygame.K_RIGHT]

    ```




##### def should_toggle_debug_hud(self) -&gt; bool:

??? note "View Source"
    ```python
            def should_toggle_debug_hud(self) -> bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_BACKQUOTE):
                        return True

                return False

    ```




##### def is_click_initialized(self) -&gt; bool:

??? note "View Source"
    ```python
            def is_click_initialized(self) -> bool:
                for event in self._events:
                    if not event.type == pygame.MOUSEBUTTONDOWN:
                        continue

                    return pygame.mouse.get_pressed(num_buttons=3)[0]

                return False

    ```




##### def is_mouse_down(self) -&gt; bool:

??? note "View Source"
    ```python
            def is_mouse_down(self) -> bool:
                return pygame.mouse.get_pressed(num_buttons=3)[0]

    ```




##### def render(self, surface: pygame.Surface) -&gt; None:

??? note "View Source"
    ```python
            def render(self, surface: pygame.Surface) -> None:
                pass

    ```



### GameObject

#### class `GameObject` (abc.ABC):

??? note "View Source"
    ```python
        class GameObject(ABC):
            """
            Interface for anything representing an object in the scene.
            """

            @abstractmethod
            def tick(self) -> None:
                pass

            @abstractmethod
            def render(self, surface: Surface) -> None:
                pass

    ```

Interface for anything representing an object in the scene.


@abstractmethod

##### def tick(self) -&gt; None:

??? note "View Source"
    ```python
            @abstractmethod
            def tick(self) -> None:
                pass

    ```



@abstractmethod

##### def render(self, surface: pygame.Surface) -&gt; None:

??? note "View Source"
    ```python
            @abstractmethod
            def render(self, surface: Surface) -> None:
                pass

    ```



### GameObjectsCollection

#### class `GameObjectsCollection` :

??? note "View Source"
    ```python
        class GameObjectsCollection:
            """
            Data structure that allows you to keep track of objects in the scene.
            """

            _game_objects: List[GameObject]

            def __init__(self) -> None:
                self._game_objects = []

            def add(self, game_object: GameObject) -> None:
                self._game_objects.append(game_object)

            def apply(self, func: Callable[[GameObject], None]) -> None:
                for game_object in self._game_objects:
                    func(game_object)

    ```

Data structure that allows you to keep track of objects in the scene.



##### GameObjectsCollection():

??? note "View Source"
    ```python
            def __init__(self) -> None:
                self._game_objects = []

    ```




##### def add(self, game_object: seagulls.engine._game_object.GameObject) -&gt; None:

??? note "View Source"
    ```python
            def add(self, game_object: GameObject) -> None:
                self._game_objects.append(game_object)

    ```




##### def apply(
    self,
    func: Callable[[seagulls.engine._game_object.GameObject], NoneType]
) -&gt; None:

??? note "View Source"
    ```python
            def apply(self, func: Callable[[GameObject], None]) -> None:
                for game_object in self._game_objects:
                    func(game_object)

    ```



### GameSettings

#### class `GameSettings` :

??? note "View Source"
    ```python
        class GameSettings:

            def get_setting(self, name, default=None) -> Any:
                data = self._load_yaml()
                return data.get(name, default)

            @lru_cache()
            def _load_yaml(self) -> Dict[str, Any]:
                file = Path.home() / ".config/seagulls.yaml"
                if not file.exists():
                    file.touch()

                return yaml.safe_load(file.read_text()) or {}

    ```




##### GameSettings():





##### def get_setting(self, name, default=None) -&gt; Any:

??? note "View Source"
    ```python
            def get_setting(self, name, default=None) -> Any:
                data = self._load_yaml()
                return data.get(name, default)

    ```



### Rect

#### class `Rect` :


Rect(left, top, width, height) -&gt; Rect
Rect((left, top), (width, height)) -&gt; Rect
Rect(object) -&gt; Rect
pygame object for storing rectangular coordinates



##### Rect(*args, **kwargs):





##### def normalize(unknown):


normalize() -&gt; None
correct negative sizes



##### def clip(unknown):


clip(Rect) -&gt; Rect
crops a rectangle inside another



##### def clipline(unknown):


clipline(x1, y1, x2, y2) -&gt; ((cx1, cy1), (cx2, cy2))
clipline(x1, y1, x2, y2) -&gt; ()
clipline((x1, y1), (x2, y2)) -&gt; ((cx1, cy1), (cx2, cy2))
clipline((x1, y1), (x2, y2)) -&gt; ()
clipline((x1, y1, x2, y2)) -&gt; ((cx1, cy1), (cx2, cy2))
clipline((x1, y1, x2, y2)) -&gt; ()
clipline(((x1, y1), (x2, y2))) -&gt; ((cx1, cy1), (cx2, cy2))
clipline(((x1, y1), (x2, y2))) -&gt; ()
crops a line inside a rectangle



##### def clamp(unknown):


clamp(Rect) -&gt; Rect
moves the rectangle inside another



##### def clamp_ip(unknown):


clamp_ip(Rect) -&gt; None
moves the rectangle inside another, in place



##### def copy(unknown):


copy() -&gt; Rect
copy the rectangle



##### def fit(unknown):


fit(Rect) -&gt; Rect
resize and move a rectangle with aspect ratio



##### def move(unknown):


move(x, y) -&gt; Rect
moves the rectangle



##### def update(unknown):


update(left, top, width, height) -&gt; None
update((left, top), (width, height)) -&gt; None
update(object) -&gt; None
sets the position and size of the rectangle



##### def inflate(unknown):


inflate(x, y) -&gt; Rect
grow or shrink the rectangle size



##### def union(unknown):


union(Rect) -&gt; Rect
joins two rectangles into one



##### def unionall(unknown):


unionall(Rect_sequence) -&gt; Rect
the union of many rectangles



##### def move_ip(unknown):


move_ip(x, y) -&gt; None
moves the rectangle, in place



##### def inflate_ip(unknown):


inflate_ip(x, y) -&gt; None
grow or shrink the rectangle size, in place



##### def union_ip(unknown):


union_ip(Rect) -&gt; None
joins two rectangles into one, in place



##### def unionall_ip(unknown):


unionall_ip(Rect_sequence) -&gt; None
the union of many rectangles, in place



##### def collidepoint(unknown):


collidepoint(x, y) -&gt; bool
collidepoint((x,y)) -&gt; bool
test if a point is inside a rectangle



##### def colliderect(unknown):


colliderect(Rect) -&gt; bool
test if two rectangles overlap



##### def collidelist(unknown):


collidelist(list) -&gt; index
test if one rectangle in a list intersects



##### def collidelistall(unknown):


collidelistall(list) -&gt; indices
test if all rectangles in a list intersect



##### def collidedict(unknown):


collidedict(dict) -&gt; (key, value)
collidedict(dict) -&gt; None
collidedict(dict, use_values=0) -&gt; (key, value)
collidedict(dict, use_values=0) -&gt; None
test if one rectangle in a dictionary intersects



##### def collidedictall(unknown):


collidedictall(dict) -&gt; [(key, value), ...]
collidedictall(dict, use_values=0) -&gt; [(key, value), ...]
test if all rectangles in a dictionary intersect



##### def contains(unknown):


contains(Rect) -&gt; bool
test if one rectangle is inside another


[# ](#Rect.x){: #Rect.x }
 x 



[# ](#Rect.y){: #Rect.y }
 y 



[# ](#Rect.w){: #Rect.w }
 w 



[# ](#Rect.h){: #Rect.h }
 h 



[# ](#Rect.width){: #Rect.width }
 width 



[# ](#Rect.height){: #Rect.height }
 height 



[# ](#Rect.top){: #Rect.top }
 top 



[# ](#Rect.left){: #Rect.left }
 left 



[# ](#Rect.bottom){: #Rect.bottom }
 bottom 



[# ](#Rect.right){: #Rect.right }
 right 



[# ](#Rect.centerx){: #Rect.centerx }
 centerx 



[# ](#Rect.centery){: #Rect.centery }
 centery 



[# ](#Rect.topleft){: #Rect.topleft }
 topleft 



[# ](#Rect.topright){: #Rect.topright }
 topright 



[# ](#Rect.bottomleft){: #Rect.bottomleft }
 bottomleft 



[# ](#Rect.bottomright){: #Rect.bottomright }
 bottomright 



[# ](#Rect.midtop){: #Rect.midtop }
 midtop 



[# ](#Rect.midleft){: #Rect.midleft }
 midleft 



[# ](#Rect.midbottom){: #Rect.midbottom }
 midbottom 



[# ](#Rect.midright){: #Rect.midright }
 midright 



[# ](#Rect.size){: #Rect.size }
 size 



[# ](#Rect.center){: #Rect.center }
 center 



### Surface

#### class `Surface` :


Surface((width, height), flags=0, depth=0, masks=None) -&gt; Surface
Surface((width, height), flags=0, Surface) -&gt; Surface
pygame object for representing images



##### Surface(*args, **kwargs):





##### def get_at(unknown):


get_at((x, y)) -&gt; Color
get the color value at a single pixel



##### def set_at(unknown):


set_at((x, y), Color) -&gt; None
set the color value for a single pixel



##### def get_at_mapped(unknown):


get_at_mapped((x, y)) -&gt; Color
get the mapped color value at a single pixel



##### def map_rgb(unknown):


map_rgb(Color) -&gt; mapped_int
convert a color into a mapped color value



##### def unmap_rgb(unknown):


unmap_rgb(mapped_int) -&gt; Color
convert a mapped integer color value into a Color



##### def get_palette(unknown):


get_palette() -&gt; [RGB, RGB, RGB, ...]
get the color index palette for an 8-bit Surface



##### def get_palette_at(unknown):


get_palette_at(index) -&gt; RGB
get the color for a single entry in a palette



##### def set_palette(unknown):


set_palette([RGB, RGB, RGB, ...]) -&gt; None
set the color palette for an 8-bit Surface



##### def set_palette_at(unknown):


set_palette_at(index, RGB) -&gt; None
set the color for a single index in an 8-bit Surface palette



##### def lock(unknown):


lock() -&gt; None
lock the Surface memory for pixel access



##### def unlock(unknown):


unlock() -&gt; None
unlock the Surface memory from pixel access



##### def mustlock(unknown):


mustlock() -&gt; bool
test if the Surface requires locking



##### def get_locked(unknown):


get_locked() -&gt; bool
test if the Surface is current locked



##### def get_locks(unknown):


get_locks() -&gt; tuple
Gets the locks for the Surface



##### def set_colorkey(unknown):


set_colorkey(Color, flags=0) -&gt; None
set_colorkey(None) -&gt; None
Set the transparent colorkey



##### def get_colorkey(unknown):


get_colorkey() -&gt; RGB or None
Get the current transparent colorkey



##### def set_alpha(unknown):


set_alpha(value, flags=0) -&gt; None
set_alpha(None) -&gt; None
set the alpha value for the full Surface image



##### def get_alpha(unknown):


get_alpha() -&gt; int_value
get the current Surface transparency value



##### def get_blendmode(unknown):


Return the surface&#39;s SDL 2 blend mode



##### def copy(unknown):


copy() -&gt; Surface
create a new copy of a Surface



##### def convert(unknown):


convert(Surface=None) -&gt; Surface
convert(depth, flags=0) -&gt; Surface
convert(masks, flags=0) -&gt; Surface
change the pixel format of an image



##### def convert_alpha(unknown):


convert_alpha(Surface) -&gt; Surface
convert_alpha() -&gt; Surface
change the pixel format of an image including per pixel alphas



##### def set_clip(unknown):


set_clip(rect) -&gt; None
set_clip(None) -&gt; None
set the current clipping area of the Surface



##### def get_clip(unknown):


get_clip() -&gt; Rect
get the current clipping area of the Surface



##### def fill(unknown):


fill(color, rect=None, special_flags=0) -&gt; Rect
fill Surface with a solid color



##### def blit(unknown):


blit(source, dest, area=None, special_flags=0) -&gt; Rect
draw one image onto another



##### def blits(unknown):


blits(blit_sequence=((source, dest), ...), doreturn=1) -&gt; [Rect, ...] or None
blits(((source, dest, area), ...)) -&gt; [Rect, ...]
blits(((source, dest, area, special_flags), ...)) -&gt; [Rect, ...]
draw many images onto another



##### def scroll(unknown):


scroll(dx=0, dy=0) -&gt; None
Shift the surface image in place



##### def get_flags(unknown):


get_flags() -&gt; int
get the additional flags used for the Surface



##### def get_size(unknown):


get_size() -&gt; (width, height)
get the dimensions of the Surface



##### def get_width(unknown):


get_width() -&gt; width
get the width of the Surface



##### def get_height(unknown):


get_height() -&gt; height
get the height of the Surface



##### def get_rect(unknown):


get_rect(**kwargs) -&gt; Rect
get the rectangular area of the Surface



##### def get_pitch(unknown):


get_pitch() -&gt; int
get the number of bytes used per Surface row



##### def get_bitsize(unknown):


get_bitsize() -&gt; int
get the bit depth of the Surface pixel format



##### def get_bytesize(unknown):


get_bytesize() -&gt; int
get the bytes used per Surface pixel



##### def get_masks(unknown):


get_masks() -&gt; (R, G, B, A)
the bitmasks needed to convert between a color and a mapped integer



##### def get_shifts(unknown):


get_shifts() -&gt; (R, G, B, A)
the bit shifts needed to convert between a color and a mapped integer



##### def set_masks(unknown):


set_masks((r,g,b,a)) -&gt; None
set the bitmasks needed to convert between a color and a mapped integer



##### def set_shifts(unknown):


set_shifts((r,g,b,a)) -&gt; None
sets the bit shifts needed to convert between a color and a mapped integer



##### def get_losses(unknown):


get_losses() -&gt; (R, G, B, A)
the significant bits used to convert between a color and a mapped integer



##### def subsurface(unknown):


subsurface(Rect) -&gt; Surface
create a new surface that references its parent



##### def get_offset(unknown):


get_offset() -&gt; (x, y)
find the position of a child subsurface inside a parent



##### def get_abs_offset(unknown):


get_abs_offset() -&gt; (x, y)
find the absolute position of a child subsurface inside its top level parent



##### def get_parent(unknown):


get_parent() -&gt; Surface
find the parent of a subsurface



##### def get_abs_parent(unknown):


get_abs_parent() -&gt; Surface
find the top level parent of a subsurface



##### def get_bounding_rect(unknown):


get_bounding_rect(min_alpha = 1) -&gt; Rect
find the smallest rect containing data



##### def get_view(unknown):


get_view(&lt;kind&gt;=&#39;2&#39;) -&gt; BufferProxy
return a buffer view of the Surface&#39;s pixels.



##### def get_buffer(unknown):


get_buffer() -&gt; BufferProxy
acquires a buffer object for the pixels of the Surface.


### Color

#### class `Color` :


Color(r, g, b) -&gt; Color
Color(r, g, b, a=255) -&gt; Color
Color(color_value) -&gt; Color
pygame object for color representations



##### Color(*args, **kwargs):





##### def normalize(unknown):


normalize() -&gt; tuple
Returns the normalized RGBA values of the Color.



##### def correct_gamma(unknown):


correct_gamma (gamma) -&gt; Color
Applies a certain gamma value to the Color.



##### def set_length(unknown):


set_length(len) -&gt; None
Set the number of elements in the Color to 1,2,3, or 4.



##### def lerp(unknown):


lerp(Color, float) -&gt; Color
returns a linear interpolation to the given Color.



##### def premul_alpha(unknown):


premul_alpha() -&gt; Color
returns a Color where the r,g,b components have been multiplied by the alpha.



##### def update(unknown):


update(r, g, b) -&gt; None
update(r, g, b, a=255) -&gt; None
update(color_value) -&gt; None
Sets the elements of the color


[# ](#Color.r){: #Color.r }
 r 

r -&gt; int
Gets or sets the red value of the Color.


[# ](#Color.g){: #Color.g }
 g 

g -&gt; int
Gets or sets the green value of the Color.


[# ](#Color.b){: #Color.b }
 b 

b -&gt; int
Gets or sets the blue value of the Color.


[# ](#Color.a){: #Color.a }
 a 

a -&gt; int
Gets or sets the alpha value of the Color.


[# ](#Color.hsva){: #Color.hsva }
 hsva 

hsva -&gt; tuple
Gets or sets the HSVA representation of the Color.


[# ](#Color.hsla){: #Color.hsla }
 hsla 

hsla -&gt; tuple
Gets or sets the HSLA representation of the Color.


[# ](#Color.i1i2i3){: #Color.i1i2i3 }
 i1i2i3 

i1i2i3 -&gt; tuple
Gets or sets the I1I2I3 representation of the Color.


[# ](#Color.cmy){: #Color.cmy }
 cmy 

cmy -&gt; tuple
Gets or sets the CMY representation of the Color.


### PixelArray

#### class `PixelArray` :


PixelArray(Surface) -&gt; PixelArray
pygame object for direct pixel access of surfaces



##### PixelArray():





##### def compare(unknown):


compare(array, distance=0, weights=(0.299, 0.587, 0.114)) -&gt; PixelArray
Compares the PixelArray with another one.



##### def extract(unknown):


extract(color, distance=0, weights=(0.299, 0.587, 0.114)) -&gt; PixelArray
Extracts the passed color from the PixelArray.



##### def make_surface(unknown):


make_surface() -&gt; Surface
Creates a new Surface from the current PixelArray.



##### def close(unknown):


transpose() -&gt; PixelArray
Closes the PixelArray, and releases Surface lock.



##### def replace(unknown):


replace(color, repcolor, distance=0, weights=(0.299, 0.587, 0.114)) -&gt; None
Replaces the passed color in the PixelArray with another one.



##### def transpose(unknown):


transpose() -&gt; PixelArray
Exchanges the x and y axis.


[# ](#PixelArray.surface){: #PixelArray.surface }
 surface 

surface -&gt; Surface
Gets the Surface the PixelArray uses.


[# ](#PixelArray.itemsize){: #PixelArray.itemsize }
 itemsize 

itemsize -&gt; int
Returns the byte size of a pixel array item


[# ](#PixelArray.shape){: #PixelArray.shape }
 shape 

shape -&gt; tuple of int&#39;s
Returns the array size.


[# ](#PixelArray.strides){: #PixelArray.strides }
 strides 

strides -&gt; tuple of int&#39;s
Returns byte offsets for each array dimension.


[# ](#PixelArray.ndim){: #PixelArray.ndim }
 ndim 

ndim -&gt; int
Returns the number of dimensions.


### Vector2

#### class `Vector2` :


Vector2() -&gt; Vector2
Vector2(int) -&gt; Vector2
Vector2(float) -&gt; Vector2
Vector2(Vector2) -&gt; Vector2
Vector2(x, y) -&gt; Vector2
Vector2((x, y)) -&gt; Vector2
a 2-Dimensional Vector



##### Vector2(*args, **kwargs):





##### def length(unknown):


length() -&gt; float
returns the Euclidean length of the vector.



##### def length_squared(unknown):


length_squared() -&gt; float
returns the squared Euclidean length of the vector.



##### def magnitude(unknown):


magnitude() -&gt; float
returns the Euclidean magnitude of the vector.



##### def magnitude_squared(unknown):


magnitude_squared() -&gt; float
returns the squared magnitude of the vector.



##### def rotate(unknown):


rotate(angle) -&gt; Vector2
rotates a vector by a given angle in degrees.



##### def rotate_ip(unknown):


rotate_ip(angle) -&gt; None
rotates the vector by a given angle in degrees in place.



##### def rotate_rad(unknown):


rotate_rad(angle) -&gt; Vector2
rotates a vector by a given angle in radians.



##### def rotate_ip_rad(unknown):


rotate_ip_rad(angle) -&gt; None
rotates the vector by a given angle in radians in place.



##### def slerp(unknown):


slerp(Vector2, float) -&gt; Vector2
returns a spherical interpolation to the given vector.



##### def lerp(unknown):


lerp(Vector2, float) -&gt; Vector2
returns a linear interpolation to the given vector.



##### def normalize(unknown):


normalize() -&gt; Vector2
returns a vector with the same direction but length 1.



##### def normalize_ip(unknown):


normalize_ip() -&gt; None
normalizes the vector in place so that its length is 1.



##### def is_normalized(unknown):


is_normalized() -&gt; Bool
tests if the vector is normalized i.e. has length == 1.



##### def cross(unknown):


cross(Vector2) -&gt; Vector2
calculates the cross- or vector-product



##### def dot(unknown):


dot(Vector2) -&gt; float
calculates the dot- or scalar-product with the other vector



##### def angle_to(unknown):


angle_to(Vector2) -&gt; float
calculates the angle to a given vector in degrees.



##### def update(unknown):


update() -&gt; None
update(int) -&gt; None
update(float) -&gt; None
update(Vector2) -&gt; None
update(x, y) -&gt; None
update((x, y)) -&gt; None
Sets the coordinates of the vector.



##### def scale_to_length(unknown):


scale_to_length(float) -&gt; None
scales the vector to a given length.



##### def reflect(unknown):


reflect(Vector2) -&gt; Vector2
returns a vector reflected of a given normal.



##### def reflect_ip(unknown):


reflect_ip(Vector2) -&gt; None
reflect the vector of a given normal in place.



##### def distance_to(unknown):


distance_to(Vector2) -&gt; float
calculates the Euclidean distance to a given vector.



##### def distance_squared_to(unknown):


distance_squared_to(Vector2) -&gt; float
calculates the squared Euclidean distance to a given vector.



##### def elementwise(unknown):


elementwise() -&gt; VectorElementwiseProxy
The next operation will be performed elementwise.



##### def as_polar(unknown):


as_polar() -&gt; (r, phi)
returns a tuple with radial distance and azimuthal angle.



##### def from_polar(unknown):


from_polar((r, phi)) -&gt; None
Sets x and y from a polar coordinates tuple.



##### def project(unknown):


project(Vector2) -&gt; Vector2
projects a vector onto another.


[# ](#Vector2.epsilon){: #Vector2.epsilon }
 epsilon 

small value used in comparisons


[# ](#Vector2.x){: #Vector2.x }
 x 



[# ](#Vector2.y){: #Vector2.y }
 y 



### Vector3

#### class `Vector3` :


Vector3() -&gt; Vector3
Vector3(int) -&gt; Vector3
Vector3(float) -&gt; Vector3
Vector3(Vector3) -&gt; Vector3
Vector3(x, y, z) -&gt; Vector3
Vector3((x, y, z)) -&gt; Vector3
a 3-Dimensional Vector



##### Vector3(*args, **kwargs):





##### def length(unknown):


length() -&gt; float
returns the Euclidean length of the vector.



##### def length_squared(unknown):


length_squared() -&gt; float
returns the squared Euclidean length of the vector.



##### def magnitude(unknown):


magnitude() -&gt; float
returns the Euclidean magnitude of the vector.



##### def magnitude_squared(unknown):


magnitude_squared() -&gt; float
returns the squared Euclidean magnitude of the vector.



##### def rotate(unknown):


rotate(angle, Vector3) -&gt; Vector3
rotates a vector by a given angle in degrees.



##### def rotate_ip(unknown):


rotate_ip(angle, Vector3) -&gt; None
rotates the vector by a given angle in degrees in place.



##### def rotate_rad(unknown):


rotate_rad(angle, Vector3) -&gt; Vector3
rotates a vector by a given angle in radians.



##### def rotate_ip_rad(unknown):


rotate_ip_rad(angle, Vector3) -&gt; None
rotates the vector by a given angle in radians in place.



##### def rotate_x(unknown):


rotate_x(angle) -&gt; Vector3
rotates a vector around the x-axis by the angle in degrees.



##### def rotate_x_ip(unknown):


rotate_x_ip(angle) -&gt; None
rotates the vector around the x-axis by the angle in degrees in place.



##### def rotate_x_rad(unknown):


rotate_x_rad(angle) -&gt; Vector3
rotates a vector around the x-axis by the angle in radians.



##### def rotate_x_ip_rad(unknown):


rotate_x_ip_rad(angle) -&gt; None
rotates the vector around the x-axis by the angle in radians in place.



##### def rotate_y(unknown):


rotate_y(angle) -&gt; Vector3
rotates a vector around the y-axis by the angle in degrees.



##### def rotate_y_ip(unknown):


rotate_y_ip(angle) -&gt; None
rotates the vector around the y-axis by the angle in degrees in place.



##### def rotate_y_rad(unknown):


rotate_y_rad(angle) -&gt; Vector3
rotates a vector around the y-axis by the angle in radians.



##### def rotate_y_ip_rad(unknown):


rotate_y_ip_rad(angle) -&gt; None
rotates the vector around the y-axis by the angle in radians in place.



##### def rotate_z(unknown):


rotate_z(angle) -&gt; Vector3
rotates a vector around the z-axis by the angle in degrees.



##### def rotate_z_ip(unknown):


rotate_z_ip(angle) -&gt; None
rotates the vector around the z-axis by the angle in degrees in place.



##### def rotate_z_rad(unknown):


rotate_z_rad(angle) -&gt; Vector3
rotates a vector around the z-axis by the angle in radians.



##### def rotate_z_ip_rad(unknown):


rotate_z_ip_rad(angle) -&gt; None
rotates the vector around the z-axis by the angle in radians in place.



##### def slerp(unknown):


slerp(Vector3, float) -&gt; Vector3
returns a spherical interpolation to the given vector.



##### def lerp(unknown):


lerp(Vector3, float) -&gt; Vector3
returns a linear interpolation to the given vector.



##### def normalize(unknown):


normalize() -&gt; Vector3
returns a vector with the same direction but length 1.



##### def normalize_ip(unknown):


normalize_ip() -&gt; None
normalizes the vector in place so that its length is 1.



##### def is_normalized(unknown):


is_normalized() -&gt; Bool
tests if the vector is normalized i.e. has length == 1.



##### def cross(unknown):


cross(Vector3) -&gt; Vector3
calculates the cross- or vector-product



##### def dot(unknown):


dot(Vector3) -&gt; float
calculates the dot- or scalar-product with the other vector



##### def angle_to(unknown):


angle_to(Vector3) -&gt; float
calculates the angle to a given vector in degrees.



##### def update(unknown):


update() -&gt; None
update(int) -&gt; None
update(float) -&gt; None
update(Vector3) -&gt; None
update(x, y, z) -&gt; None
update((x, y, z)) -&gt; None
Sets the coordinates of the vector.



##### def scale_to_length(unknown):


scale_to_length(float) -&gt; None
scales the vector to a given length.



##### def reflect(unknown):


reflect(Vector3) -&gt; Vector3
returns a vector reflected of a given normal.



##### def reflect_ip(unknown):


reflect_ip(Vector3) -&gt; None
reflect the vector of a given normal in place.



##### def distance_to(unknown):


distance_to(Vector3) -&gt; float
calculates the Euclidean distance to a given vector.



##### def distance_squared_to(unknown):


distance_squared_to(Vector3) -&gt; float
calculates the squared Euclidean distance to a given vector.



##### def elementwise(unknown):


elementwise() -&gt; VectorElementwiseProxy
The next operation will be performed elementwise.



##### def as_spherical(unknown):


as_spherical() -&gt; (r, theta, phi)
returns a tuple with radial distance, inclination and azimuthal angle.



##### def from_spherical(unknown):


from_spherical((r, theta, phi)) -&gt; None
Sets x, y and z from a spherical coordinates 3-tuple.



##### def project(unknown):


project(Vector3) -&gt; Vector3
projects a vector onto another.


[# ](#Vector3.epsilon){: #Vector3.epsilon }
 epsilon 

small value used in comparisons


[# ](#Vector3.x){: #Vector3.x }
 x 



[# ](#Vector3.y){: #Vector3.y }
 y 



[# ](#Vector3.z){: #Vector3.z }
 z 



