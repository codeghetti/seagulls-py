---
title: "API Docs: seagulls.engine"
---


# [seagulls](../seagulls).engine

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

## flag_from_string()

```python
def flag_from_string(value: str) -> int:
```


??? note "View Source"
    ```python
        def flag_from_string(value: str) -> int:
            if not isinstance(value, str):
                raise ValueError(f"Value must be a string of 0s and 1s: {value}")

            return int(value, 2)

    ```


## CollidableObject

```python
@dataclass(frozen=True)
class CollidableObject:
```

CollidableObject(layer: int, mask: int)

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


### \_\_init\_\_()

```python
CollidableObject(layer: int, mask: int):
```




### filter_by_mask()

```python
def filter_by_mask(
    self,
    targets: Tuple[seagulls.engine._collisions.CollidableObject, ...]
) -> Tuple[seagulls.engine._collisions.CollidableObject, ...]:
```


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


### is_in_mask()

```python
def is_in_mask(self, target: seagulls.engine._collisions.CollidableObject) -> bool:
```


??? note "View Source"
    ```python
            def is_in_mask(self, target: "CollidableObject") -> bool:
                logger.debug(f"targeting items located in mask: {self.mask:b}")
                logger.debug(f"target is located in layer: {target.layer:b}")
                logger.debug(f"& result: {self.mask & target.layer:b}")
                return self.mask & target.layer > 0

    ```


## IGameScene

```python
class IGameScene(abc.ABC):
```

This class is for X and Y.

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


### start()

```python
@abstractmethod
def start(self) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def start(self) -> None:
                pass

    ```


### should_quit()

```python
@abstractmethod
def should_quit(self) -> bool:
```


??? note "View Source"
    ```python
            @abstractmethod
            def should_quit(self) -> bool:
                pass

    ```


### tick()

```python
@abstractmethod
def tick(self) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def tick(self) -> None:
                pass

    ```


## IProvideGameScenes

```python
class IProvideGameScenes(abc.ABC):
```

Helper class that provides a standard way to create an ABC using
inheritance.

??? note "View Source"
    ```python
        class IProvideGameScenes(ABC):

            @abstractmethod
            def get_scene(self) -> IGameScene:
                pass

    ```


### get_scene()

```python
@abstractmethod
def get_scene(self) -> seagulls.engine._game_scene.IGameScene:
```


??? note "View Source"
    ```python
            @abstractmethod
            def get_scene(self) -> IGameScene:
                pass

    ```


## IProvideGameSessions

```python
class IProvideGameSessions(abc.ABC):
```

Helper class that provides a standard way to create an ABC using
inheritance.

??? note "View Source"
    ```python
        class IProvideGameSessions(ABC):

            @abstractmethod
            def get_session(self, scene: str) -> IGameSession:
                pass

    ```


### get_session()

```python
@abstractmethod
def get_session(self, scene: str) -> seagulls.engine._game_session.IGameSession:
```


??? note "View Source"
    ```python
            @abstractmethod
            def get_session(self, scene: str) -> IGameSession:
                pass

    ```


## IGameSession

```python
class IGameSession(abc.ABC):
```

Helper class that provides a standard way to create an ABC using
inheritance.

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


### start()

```python
@abstractmethod
def start(self) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def start(self) -> None:
                pass

    ```


### wait_for_completion()

```python
@abstractmethod
def wait_for_completion(self) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def wait_for_completion(self) -> None:
                pass

    ```


### stop()

```python
@abstractmethod
def stop(self) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def stop(self) -> None:
                pass

    ```


## SurfaceRenderer

```python
class SurfaceRenderer:
```


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


### \_\_init\_\_()

```python
SurfaceRenderer():
```




### start()

```python
def start(self) -> None:
```


??? note "View Source"
    ```python
            def start(self) -> None:
                self._get_surface()

    ```


### render()

```python
def render(self, surface: pygame.Surface) -> None:
```


??? note "View Source"
    ```python
            def render(self, surface: Surface) -> None:
                self._get_surface().blit(surface, (0, 0))
                pygame.display.flip()

    ```


## GameClock

```python
class GameClock(seagulls.engine._game_object.GameObject):
```

Interface for anything representing an object in the scene.

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


### \_\_init\_\_()

```python
GameClock():
```


??? note "View Source"
    ```python
            def __init__(self):
                self._clock = Clock()
                self._ticks = 0
                self._delta = 0

    ```


### tick()

```python
def tick(self) -> None:
```


??? note "View Source"
    ```python
            def tick(self) -> None:
                self._delta = self._clock.tick()

    ```


### render()

```python
def render(self, surface: pygame.Surface) -> None:
```


??? note "View Source"
    ```python
            def render(self, surface: Surface) -> None:
                pass

    ```


### get_time()

```python
def get_time(self) -> int:
```


??? note "View Source"
    ```python
            def get_time(self) -> int:
                return self._delta

    ```


### get_fps()

```python
def get_fps(self) -> float:
```


??? note "View Source"
    ```python
            def get_fps(self) -> float:
                return self._clock.get_fps()

    ```


## GameControls

```python
class GameControls(seagulls.engine._game_object.GameObject):
```

Interface for anything representing an object in the scene.

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


### \_\_init\_\_()

```python
GameControls():
```


??? note "View Source"
    ```python
            def __init__(self):
                self._events = []

    ```


### tick()

```python
def tick(self):
```


??? note "View Source"
    ```python
            def tick(self):
                self._events = pygame.event.get()

    ```


### should_quit()

```python
def should_quit(self) -> bool:
```


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


### should_fire()

```python
def should_fire(self) -> bool:
```


??? note "View Source"
    ```python
            def should_fire(self) -> bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_SPACE):
                        return True

                return False

    ```


### is_left_moving()

```python
def is_left_moving(self) -> bool:
```


??? note "View Source"
    ```python
            def is_left_moving(self) -> bool:
                return pygame.key.get_pressed()[pygame.K_LEFT]

    ```


### is_right_moving()

```python
def is_right_moving(self) -> bool:
```


??? note "View Source"
    ```python
            def is_right_moving(self) -> bool:
                return pygame.key.get_pressed()[pygame.K_RIGHT]

    ```


### should_toggle_debug_hud()

```python
def should_toggle_debug_hud(self) -> bool:
```


??? note "View Source"
    ```python
            def should_toggle_debug_hud(self) -> bool:
                for event in self._events:
                    if self._is_key_down_event(event, pygame.K_BACKQUOTE):
                        return True

                return False

    ```


### is_click_initialized()

```python
def is_click_initialized(self) -> bool:
```


??? note "View Source"
    ```python
            def is_click_initialized(self) -> bool:
                for event in self._events:
                    if not event.type == pygame.MOUSEBUTTONDOWN:
                        continue

                    return pygame.mouse.get_pressed(num_buttons=3)[0]

                return False

    ```


### is_mouse_down()

```python
def is_mouse_down(self) -> bool:
```


??? note "View Source"
    ```python
            def is_mouse_down(self) -> bool:
                return pygame.mouse.get_pressed(num_buttons=3)[0]

    ```


### render()

```python
def render(self, surface: pygame.Surface) -> None:
```


??? note "View Source"
    ```python
            def render(self, surface: pygame.Surface) -> None:
                pass

    ```


## GameObject

```python
class GameObject(abc.ABC):
```

Interface for anything representing an object in the scene.

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


### tick()

```python
@abstractmethod
def tick(self) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def tick(self) -> None:
                pass

    ```


### render()

```python
@abstractmethod
def render(self, surface: pygame.Surface) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def render(self, surface: Surface) -> None:
                pass

    ```


## GameObjectsCollection

```python
class GameObjectsCollection:
```

Data structure that allows you to keep track of objects in the scene.

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


### \_\_init\_\_()

```python
GameObjectsCollection():
```


??? note "View Source"
    ```python
            def __init__(self) -> None:
                self._game_objects = []

    ```


### add()

```python
def add(self, game_object: seagulls.engine._game_object.GameObject) -> None:
```


??? note "View Source"
    ```python
            def add(self, game_object: GameObject) -> None:
                self._game_objects.append(game_object)

    ```


### apply()

```python
def apply(
    self,
    func: Callable[[seagulls.engine._game_object.GameObject], NoneType]
) -> None:
```


??? note "View Source"
    ```python
            def apply(self, func: Callable[[GameObject], None]) -> None:
                for game_object in self._game_objects:
                    func(game_object)

    ```


## GameSettings

```python
class GameSettings:
```


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


### \_\_init\_\_()

```python
GameSettings():
```




### get_setting()

```python
def get_setting(self, name, default=None) -> Any:
```


??? note "View Source"
    ```python
            def get_setting(self, name, default=None) -> Any:
                data = self._load_yaml()
                return data.get(name, default)

    ```


## Rect

```python
class Rect:
```

Rect(left, top, width, height) -&gt; Rect
Rect((left, top), (width, height)) -&gt; Rect
Rect(object) -&gt; Rect
pygame object for storing rectangular coordinates



### \_\_init\_\_()

```python
Rect(*args, **kwargs):
```




### normalize()

```python
def normalize(unknown):
```

normalize() -&gt; None
correct negative sizes



### clip()

```python
def clip(unknown):
```

clip(Rect) -&gt; Rect
crops a rectangle inside another



### clipline()

```python
def clipline(unknown):
```

clipline(x1, y1, x2, y2) -&gt; ((cx1, cy1), (cx2, cy2))
clipline(x1, y1, x2, y2) -&gt; ()
clipline((x1, y1), (x2, y2)) -&gt; ((cx1, cy1), (cx2, cy2))
clipline((x1, y1), (x2, y2)) -&gt; ()
clipline((x1, y1, x2, y2)) -&gt; ((cx1, cy1), (cx2, cy2))
clipline((x1, y1, x2, y2)) -&gt; ()
clipline(((x1, y1), (x2, y2))) -&gt; ((cx1, cy1), (cx2, cy2))
clipline(((x1, y1), (x2, y2))) -&gt; ()
crops a line inside a rectangle



### clamp()

```python
def clamp(unknown):
```

clamp(Rect) -&gt; Rect
moves the rectangle inside another



### clamp_ip()

```python
def clamp_ip(unknown):
```

clamp_ip(Rect) -&gt; None
moves the rectangle inside another, in place



### copy()

```python
def copy(unknown):
```

copy() -&gt; Rect
copy the rectangle



### fit()

```python
def fit(unknown):
```

fit(Rect) -&gt; Rect
resize and move a rectangle with aspect ratio



### move()

```python
def move(unknown):
```

move(x, y) -&gt; Rect
moves the rectangle



### update()

```python
def update(unknown):
```

update(left, top, width, height) -&gt; None
update((left, top), (width, height)) -&gt; None
update(object) -&gt; None
sets the position and size of the rectangle



### inflate()

```python
def inflate(unknown):
```

inflate(x, y) -&gt; Rect
grow or shrink the rectangle size



### union()

```python
def union(unknown):
```

union(Rect) -&gt; Rect
joins two rectangles into one



### unionall()

```python
def unionall(unknown):
```

unionall(Rect_sequence) -&gt; Rect
the union of many rectangles



### move_ip()

```python
def move_ip(unknown):
```

move_ip(x, y) -&gt; None
moves the rectangle, in place



### inflate_ip()

```python
def inflate_ip(unknown):
```

inflate_ip(x, y) -&gt; None
grow or shrink the rectangle size, in place



### union_ip()

```python
def union_ip(unknown):
```

union_ip(Rect) -&gt; None
joins two rectangles into one, in place



### unionall_ip()

```python
def unionall_ip(unknown):
```

unionall_ip(Rect_sequence) -&gt; None
the union of many rectangles, in place



### collidepoint()

```python
def collidepoint(unknown):
```

collidepoint(x, y) -&gt; bool
collidepoint((x,y)) -&gt; bool
test if a point is inside a rectangle



### colliderect()

```python
def colliderect(unknown):
```

colliderect(Rect) -&gt; bool
test if two rectangles overlap



### collidelist()

```python
def collidelist(unknown):
```

collidelist(list) -&gt; index
test if one rectangle in a list intersects



### collidelistall()

```python
def collidelistall(unknown):
```

collidelistall(list) -&gt; indices
test if all rectangles in a list intersect



### collidedict()

```python
def collidedict(unknown):
```

collidedict(dict) -&gt; (key, value)
collidedict(dict) -&gt; None
collidedict(dict, use_values=0) -&gt; (key, value)
collidedict(dict, use_values=0) -&gt; None
test if one rectangle in a dictionary intersects



### collidedictall()

```python
def collidedictall(unknown):
```

collidedictall(dict) -&gt; [(key, value), ...]
collidedictall(dict, use_values=0) -&gt; [(key, value), ...]
test if all rectangles in a dictionary intersect



### contains()

```python
def contains(unknown):
```

contains(Rect) -&gt; bool
test if one rectangle is inside another



### x

```python
x
```



### y

```python
y
```



### w

```python
w
```



### h

```python
h
```



### width

```python
width
```



### height

```python
height
```



### top

```python
top
```



### left

```python
left
```



### bottom

```python
bottom
```



### right

```python
right
```



### centerx

```python
centerx
```



### centery

```python
centery
```



### topleft

```python
topleft
```



### topright

```python
topright
```



### bottomleft

```python
bottomleft
```



### bottomright

```python
bottomright
```



### midtop

```python
midtop
```



### midleft

```python
midleft
```



### midbottom

```python
midbottom
```



### midright

```python
midright
```



### size

```python
size
```



### center

```python
center
```



## Surface

```python
class Surface:
```

Surface((width, height), flags=0, depth=0, masks=None) -&gt; Surface
Surface((width, height), flags=0, Surface) -&gt; Surface
pygame object for representing images



### \_\_init\_\_()

```python
Surface(*args, **kwargs):
```




### get_at()

```python
def get_at(unknown):
```

get_at((x, y)) -&gt; Color
get the color value at a single pixel



### set_at()

```python
def set_at(unknown):
```

set_at((x, y), Color) -&gt; None
set the color value for a single pixel



### get_at_mapped()

```python
def get_at_mapped(unknown):
```

get_at_mapped((x, y)) -&gt; Color
get the mapped color value at a single pixel



### map_rgb()

```python
def map_rgb(unknown):
```

map_rgb(Color) -&gt; mapped_int
convert a color into a mapped color value



### unmap_rgb()

```python
def unmap_rgb(unknown):
```

unmap_rgb(mapped_int) -&gt; Color
convert a mapped integer color value into a Color



### get_palette()

```python
def get_palette(unknown):
```

get_palette() -&gt; [RGB, RGB, RGB, ...]
get the color index palette for an 8-bit Surface



### get_palette_at()

```python
def get_palette_at(unknown):
```

get_palette_at(index) -&gt; RGB
get the color for a single entry in a palette



### set_palette()

```python
def set_palette(unknown):
```

set_palette([RGB, RGB, RGB, ...]) -&gt; None
set the color palette for an 8-bit Surface



### set_palette_at()

```python
def set_palette_at(unknown):
```

set_palette_at(index, RGB) -&gt; None
set the color for a single index in an 8-bit Surface palette



### lock()

```python
def lock(unknown):
```

lock() -&gt; None
lock the Surface memory for pixel access



### unlock()

```python
def unlock(unknown):
```

unlock() -&gt; None
unlock the Surface memory from pixel access



### mustlock()

```python
def mustlock(unknown):
```

mustlock() -&gt; bool
test if the Surface requires locking



### get_locked()

```python
def get_locked(unknown):
```

get_locked() -&gt; bool
test if the Surface is current locked



### get_locks()

```python
def get_locks(unknown):
```

get_locks() -&gt; tuple
Gets the locks for the Surface



### set_colorkey()

```python
def set_colorkey(unknown):
```

set_colorkey(Color, flags=0) -&gt; None
set_colorkey(None) -&gt; None
Set the transparent colorkey



### get_colorkey()

```python
def get_colorkey(unknown):
```

get_colorkey() -&gt; RGB or None
Get the current transparent colorkey



### set_alpha()

```python
def set_alpha(unknown):
```

set_alpha(value, flags=0) -&gt; None
set_alpha(None) -&gt; None
set the alpha value for the full Surface image



### get_alpha()

```python
def get_alpha(unknown):
```

get_alpha() -&gt; int_value
get the current Surface transparency value



### get_blendmode()

```python
def get_blendmode(unknown):
```

Return the surface&#39;s SDL 2 blend mode



### copy()

```python
def copy(unknown):
```

copy() -&gt; Surface
create a new copy of a Surface



### convert()

```python
def convert(unknown):
```

convert(Surface=None) -&gt; Surface
convert(depth, flags=0) -&gt; Surface
convert(masks, flags=0) -&gt; Surface
change the pixel format of an image



### convert_alpha()

```python
def convert_alpha(unknown):
```

convert_alpha(Surface) -&gt; Surface
convert_alpha() -&gt; Surface
change the pixel format of an image including per pixel alphas



### set_clip()

```python
def set_clip(unknown):
```

set_clip(rect) -&gt; None
set_clip(None) -&gt; None
set the current clipping area of the Surface



### get_clip()

```python
def get_clip(unknown):
```

get_clip() -&gt; Rect
get the current clipping area of the Surface



### fill()

```python
def fill(unknown):
```

fill(color, rect=None, special_flags=0) -&gt; Rect
fill Surface with a solid color



### blit()

```python
def blit(unknown):
```

blit(source, dest, area=None, special_flags=0) -&gt; Rect
draw one image onto another



### blits()

```python
def blits(unknown):
```

blits(blit_sequence=((source, dest), ...), doreturn=1) -&gt; [Rect, ...] or None
blits(((source, dest, area), ...)) -&gt; [Rect, ...]
blits(((source, dest, area, special_flags), ...)) -&gt; [Rect, ...]
draw many images onto another



### scroll()

```python
def scroll(unknown):
```

scroll(dx=0, dy=0) -&gt; None
Shift the surface image in place



### get_flags()

```python
def get_flags(unknown):
```

get_flags() -&gt; int
get the additional flags used for the Surface



### get_size()

```python
def get_size(unknown):
```

get_size() -&gt; (width, height)
get the dimensions of the Surface



### get_width()

```python
def get_width(unknown):
```

get_width() -&gt; width
get the width of the Surface



### get_height()

```python
def get_height(unknown):
```

get_height() -&gt; height
get the height of the Surface



### get_rect()

```python
def get_rect(unknown):
```

get_rect(**kwargs) -&gt; Rect
get the rectangular area of the Surface



### get_pitch()

```python
def get_pitch(unknown):
```

get_pitch() -&gt; int
get the number of bytes used per Surface row



### get_bitsize()

```python
def get_bitsize(unknown):
```

get_bitsize() -&gt; int
get the bit depth of the Surface pixel format



### get_bytesize()

```python
def get_bytesize(unknown):
```

get_bytesize() -&gt; int
get the bytes used per Surface pixel



### get_masks()

```python
def get_masks(unknown):
```

get_masks() -&gt; (R, G, B, A)
the bitmasks needed to convert between a color and a mapped integer



### get_shifts()

```python
def get_shifts(unknown):
```

get_shifts() -&gt; (R, G, B, A)
the bit shifts needed to convert between a color and a mapped integer



### set_masks()

```python
def set_masks(unknown):
```

set_masks((r,g,b,a)) -&gt; None
set the bitmasks needed to convert between a color and a mapped integer



### set_shifts()

```python
def set_shifts(unknown):
```

set_shifts((r,g,b,a)) -&gt; None
sets the bit shifts needed to convert between a color and a mapped integer



### get_losses()

```python
def get_losses(unknown):
```

get_losses() -&gt; (R, G, B, A)
the significant bits used to convert between a color and a mapped integer



### subsurface()

```python
def subsurface(unknown):
```

subsurface(Rect) -&gt; Surface
create a new surface that references its parent



### get_offset()

```python
def get_offset(unknown):
```

get_offset() -&gt; (x, y)
find the position of a child subsurface inside a parent



### get_abs_offset()

```python
def get_abs_offset(unknown):
```

get_abs_offset() -&gt; (x, y)
find the absolute position of a child subsurface inside its top level parent



### get_parent()

```python
def get_parent(unknown):
```

get_parent() -&gt; Surface
find the parent of a subsurface



### get_abs_parent()

```python
def get_abs_parent(unknown):
```

get_abs_parent() -&gt; Surface
find the top level parent of a subsurface



### get_bounding_rect()

```python
def get_bounding_rect(unknown):
```

get_bounding_rect(min_alpha = 1) -&gt; Rect
find the smallest rect containing data



### get_view()

```python
def get_view(unknown):
```

get_view(&lt;kind&gt;=&#39;2&#39;) -&gt; BufferProxy
return a buffer view of the Surface&#39;s pixels.



### get_buffer()

```python
def get_buffer(unknown):
```

get_buffer() -&gt; BufferProxy
acquires a buffer object for the pixels of the Surface.



## Color

```python
class Color:
```

Color(r, g, b) -&gt; Color
Color(r, g, b, a=255) -&gt; Color
Color(color_value) -&gt; Color
pygame object for color representations



### \_\_init\_\_()

```python
Color(*args, **kwargs):
```




### normalize()

```python
def normalize(unknown):
```

normalize() -&gt; tuple
Returns the normalized RGBA values of the Color.



### correct_gamma()

```python
def correct_gamma(unknown):
```

correct_gamma (gamma) -&gt; Color
Applies a certain gamma value to the Color.



### set_length()

```python
def set_length(unknown):
```

set_length(len) -&gt; None
Set the number of elements in the Color to 1,2,3, or 4.



### lerp()

```python
def lerp(unknown):
```

lerp(Color, float) -&gt; Color
returns a linear interpolation to the given Color.



### premul_alpha()

```python
def premul_alpha(unknown):
```

premul_alpha() -&gt; Color
returns a Color where the r,g,b components have been multiplied by the alpha.



### update()

```python
def update(unknown):
```

update(r, g, b) -&gt; None
update(r, g, b, a=255) -&gt; None
update(color_value) -&gt; None
Sets the elements of the color



### r

```python
r
```

r -&gt; int
Gets or sets the red value of the Color.


### g

```python
g
```

g -&gt; int
Gets or sets the green value of the Color.


### b

```python
b
```

b -&gt; int
Gets or sets the blue value of the Color.


### a

```python
a
```

a -&gt; int
Gets or sets the alpha value of the Color.


### hsva

```python
hsva
```

hsva -&gt; tuple
Gets or sets the HSVA representation of the Color.


### hsla

```python
hsla
```

hsla -&gt; tuple
Gets or sets the HSLA representation of the Color.


### i1i2i3

```python
i1i2i3
```

i1i2i3 -&gt; tuple
Gets or sets the I1I2I3 representation of the Color.


### cmy

```python
cmy
```

cmy -&gt; tuple
Gets or sets the CMY representation of the Color.


## PixelArray

```python
class PixelArray:
```

PixelArray(Surface) -&gt; PixelArray
pygame object for direct pixel access of surfaces



### \_\_init\_\_()

```python
PixelArray():
```




### compare()

```python
def compare(unknown):
```

compare(array, distance=0, weights=(0.299, 0.587, 0.114)) -&gt; PixelArray
Compares the PixelArray with another one.



### extract()

```python
def extract(unknown):
```

extract(color, distance=0, weights=(0.299, 0.587, 0.114)) -&gt; PixelArray
Extracts the passed color from the PixelArray.



### make_surface()

```python
def make_surface(unknown):
```

make_surface() -&gt; Surface
Creates a new Surface from the current PixelArray.



### close()

```python
def close(unknown):
```

transpose() -&gt; PixelArray
Closes the PixelArray, and releases Surface lock.



### replace()

```python
def replace(unknown):
```

replace(color, repcolor, distance=0, weights=(0.299, 0.587, 0.114)) -&gt; None
Replaces the passed color in the PixelArray with another one.



### transpose()

```python
def transpose(unknown):
```

transpose() -&gt; PixelArray
Exchanges the x and y axis.



### surface

```python
surface
```

surface -&gt; Surface
Gets the Surface the PixelArray uses.


### itemsize

```python
itemsize
```

itemsize -&gt; int
Returns the byte size of a pixel array item


### shape

```python
shape
```

shape -&gt; tuple of int&#39;s
Returns the array size.


### strides

```python
strides
```

strides -&gt; tuple of int&#39;s
Returns byte offsets for each array dimension.


### ndim

```python
ndim
```

ndim -&gt; int
Returns the number of dimensions.


## Vector2

```python
class Vector2:
```

Vector2() -&gt; Vector2
Vector2(int) -&gt; Vector2
Vector2(float) -&gt; Vector2
Vector2(Vector2) -&gt; Vector2
Vector2(x, y) -&gt; Vector2
Vector2((x, y)) -&gt; Vector2
a 2-Dimensional Vector



### \_\_init\_\_()

```python
Vector2(*args, **kwargs):
```




### length()

```python
def length(unknown):
```

length() -&gt; float
returns the Euclidean length of the vector.



### length_squared()

```python
def length_squared(unknown):
```

length_squared() -&gt; float
returns the squared Euclidean length of the vector.



### magnitude()

```python
def magnitude(unknown):
```

magnitude() -&gt; float
returns the Euclidean magnitude of the vector.



### magnitude_squared()

```python
def magnitude_squared(unknown):
```

magnitude_squared() -&gt; float
returns the squared magnitude of the vector.



### rotate()

```python
def rotate(unknown):
```

rotate(angle) -&gt; Vector2
rotates a vector by a given angle in degrees.



### rotate_ip()

```python
def rotate_ip(unknown):
```

rotate_ip(angle) -&gt; None
rotates the vector by a given angle in degrees in place.



### rotate_rad()

```python
def rotate_rad(unknown):
```

rotate_rad(angle) -&gt; Vector2
rotates a vector by a given angle in radians.



### rotate_ip_rad()

```python
def rotate_ip_rad(unknown):
```

rotate_ip_rad(angle) -&gt; None
rotates the vector by a given angle in radians in place.



### slerp()

```python
def slerp(unknown):
```

slerp(Vector2, float) -&gt; Vector2
returns a spherical interpolation to the given vector.



### lerp()

```python
def lerp(unknown):
```

lerp(Vector2, float) -&gt; Vector2
returns a linear interpolation to the given vector.



### normalize()

```python
def normalize(unknown):
```

normalize() -&gt; Vector2
returns a vector with the same direction but length 1.



### normalize_ip()

```python
def normalize_ip(unknown):
```

normalize_ip() -&gt; None
normalizes the vector in place so that its length is 1.



### is_normalized()

```python
def is_normalized(unknown):
```

is_normalized() -&gt; Bool
tests if the vector is normalized i.e. has length == 1.



### cross()

```python
def cross(unknown):
```

cross(Vector2) -&gt; Vector2
calculates the cross- or vector-product



### dot()

```python
def dot(unknown):
```

dot(Vector2) -&gt; float
calculates the dot- or scalar-product with the other vector



### angle_to()

```python
def angle_to(unknown):
```

angle_to(Vector2) -&gt; float
calculates the angle to a given vector in degrees.



### update()

```python
def update(unknown):
```

update() -&gt; None
update(int) -&gt; None
update(float) -&gt; None
update(Vector2) -&gt; None
update(x, y) -&gt; None
update((x, y)) -&gt; None
Sets the coordinates of the vector.



### scale_to_length()

```python
def scale_to_length(unknown):
```

scale_to_length(float) -&gt; None
scales the vector to a given length.



### reflect()

```python
def reflect(unknown):
```

reflect(Vector2) -&gt; Vector2
returns a vector reflected of a given normal.



### reflect_ip()

```python
def reflect_ip(unknown):
```

reflect_ip(Vector2) -&gt; None
reflect the vector of a given normal in place.



### distance_to()

```python
def distance_to(unknown):
```

distance_to(Vector2) -&gt; float
calculates the Euclidean distance to a given vector.



### distance_squared_to()

```python
def distance_squared_to(unknown):
```

distance_squared_to(Vector2) -&gt; float
calculates the squared Euclidean distance to a given vector.



### elementwise()

```python
def elementwise(unknown):
```

elementwise() -&gt; VectorElementwiseProxy
The next operation will be performed elementwise.



### as_polar()

```python
def as_polar(unknown):
```

as_polar() -&gt; (r, phi)
returns a tuple with radial distance and azimuthal angle.



### from_polar()

```python
def from_polar(unknown):
```

from_polar((r, phi)) -&gt; None
Sets x and y from a polar coordinates tuple.



### project()

```python
def project(unknown):
```

project(Vector2) -&gt; Vector2
projects a vector onto another.



### epsilon

```python
epsilon
```

small value used in comparisons


### x

```python
x
```



### y

```python
y
```



## Vector3

```python
class Vector3:
```

Vector3() -&gt; Vector3
Vector3(int) -&gt; Vector3
Vector3(float) -&gt; Vector3
Vector3(Vector3) -&gt; Vector3
Vector3(x, y, z) -&gt; Vector3
Vector3((x, y, z)) -&gt; Vector3
a 3-Dimensional Vector



### \_\_init\_\_()

```python
Vector3(*args, **kwargs):
```




### length()

```python
def length(unknown):
```

length() -&gt; float
returns the Euclidean length of the vector.



### length_squared()

```python
def length_squared(unknown):
```

length_squared() -&gt; float
returns the squared Euclidean length of the vector.



### magnitude()

```python
def magnitude(unknown):
```

magnitude() -&gt; float
returns the Euclidean magnitude of the vector.



### magnitude_squared()

```python
def magnitude_squared(unknown):
```

magnitude_squared() -&gt; float
returns the squared Euclidean magnitude of the vector.



### rotate()

```python
def rotate(unknown):
```

rotate(angle, Vector3) -&gt; Vector3
rotates a vector by a given angle in degrees.



### rotate_ip()

```python
def rotate_ip(unknown):
```

rotate_ip(angle, Vector3) -&gt; None
rotates the vector by a given angle in degrees in place.



### rotate_rad()

```python
def rotate_rad(unknown):
```

rotate_rad(angle, Vector3) -&gt; Vector3
rotates a vector by a given angle in radians.



### rotate_ip_rad()

```python
def rotate_ip_rad(unknown):
```

rotate_ip_rad(angle, Vector3) -&gt; None
rotates the vector by a given angle in radians in place.



### rotate_x()

```python
def rotate_x(unknown):
```

rotate_x(angle) -&gt; Vector3
rotates a vector around the x-axis by the angle in degrees.



### rotate_x_ip()

```python
def rotate_x_ip(unknown):
```

rotate_x_ip(angle) -&gt; None
rotates the vector around the x-axis by the angle in degrees in place.



### rotate_x_rad()

```python
def rotate_x_rad(unknown):
```

rotate_x_rad(angle) -&gt; Vector3
rotates a vector around the x-axis by the angle in radians.



### rotate_x_ip_rad()

```python
def rotate_x_ip_rad(unknown):
```

rotate_x_ip_rad(angle) -&gt; None
rotates the vector around the x-axis by the angle in radians in place.



### rotate_y()

```python
def rotate_y(unknown):
```

rotate_y(angle) -&gt; Vector3
rotates a vector around the y-axis by the angle in degrees.



### rotate_y_ip()

```python
def rotate_y_ip(unknown):
```

rotate_y_ip(angle) -&gt; None
rotates the vector around the y-axis by the angle in degrees in place.



### rotate_y_rad()

```python
def rotate_y_rad(unknown):
```

rotate_y_rad(angle) -&gt; Vector3
rotates a vector around the y-axis by the angle in radians.



### rotate_y_ip_rad()

```python
def rotate_y_ip_rad(unknown):
```

rotate_y_ip_rad(angle) -&gt; None
rotates the vector around the y-axis by the angle in radians in place.



### rotate_z()

```python
def rotate_z(unknown):
```

rotate_z(angle) -&gt; Vector3
rotates a vector around the z-axis by the angle in degrees.



### rotate_z_ip()

```python
def rotate_z_ip(unknown):
```

rotate_z_ip(angle) -&gt; None
rotates the vector around the z-axis by the angle in degrees in place.



### rotate_z_rad()

```python
def rotate_z_rad(unknown):
```

rotate_z_rad(angle) -&gt; Vector3
rotates a vector around the z-axis by the angle in radians.



### rotate_z_ip_rad()

```python
def rotate_z_ip_rad(unknown):
```

rotate_z_ip_rad(angle) -&gt; None
rotates the vector around the z-axis by the angle in radians in place.



### slerp()

```python
def slerp(unknown):
```

slerp(Vector3, float) -&gt; Vector3
returns a spherical interpolation to the given vector.



### lerp()

```python
def lerp(unknown):
```

lerp(Vector3, float) -&gt; Vector3
returns a linear interpolation to the given vector.



### normalize()

```python
def normalize(unknown):
```

normalize() -&gt; Vector3
returns a vector with the same direction but length 1.



### normalize_ip()

```python
def normalize_ip(unknown):
```

normalize_ip() -&gt; None
normalizes the vector in place so that its length is 1.



### is_normalized()

```python
def is_normalized(unknown):
```

is_normalized() -&gt; Bool
tests if the vector is normalized i.e. has length == 1.



### cross()

```python
def cross(unknown):
```

cross(Vector3) -&gt; Vector3
calculates the cross- or vector-product



### dot()

```python
def dot(unknown):
```

dot(Vector3) -&gt; float
calculates the dot- or scalar-product with the other vector



### angle_to()

```python
def angle_to(unknown):
```

angle_to(Vector3) -&gt; float
calculates the angle to a given vector in degrees.



### update()

```python
def update(unknown):
```

update() -&gt; None
update(int) -&gt; None
update(float) -&gt; None
update(Vector3) -&gt; None
update(x, y, z) -&gt; None
update((x, y, z)) -&gt; None
Sets the coordinates of the vector.



### scale_to_length()

```python
def scale_to_length(unknown):
```

scale_to_length(float) -&gt; None
scales the vector to a given length.



### reflect()

```python
def reflect(unknown):
```

reflect(Vector3) -&gt; Vector3
returns a vector reflected of a given normal.



### reflect_ip()

```python
def reflect_ip(unknown):
```

reflect_ip(Vector3) -&gt; None
reflect the vector of a given normal in place.



### distance_to()

```python
def distance_to(unknown):
```

distance_to(Vector3) -&gt; float
calculates the Euclidean distance to a given vector.



### distance_squared_to()

```python
def distance_squared_to(unknown):
```

distance_squared_to(Vector3) -&gt; float
calculates the squared Euclidean distance to a given vector.



### elementwise()

```python
def elementwise(unknown):
```

elementwise() -&gt; VectorElementwiseProxy
The next operation will be performed elementwise.



### as_spherical()

```python
def as_spherical(unknown):
```

as_spherical() -&gt; (r, theta, phi)
returns a tuple with radial distance, inclination and azimuthal angle.



### from_spherical()

```python
def from_spherical(unknown):
```

from_spherical((r, theta, phi)) -&gt; None
Sets x, y and z from a spherical coordinates 3-tuple.



### project()

```python
def project(unknown):
```

project(Vector3) -&gt; Vector3
projects a vector onto another.



### epsilon

```python
epsilon
```

small value used in comparisons


### x

```python
x
```



### y

```python
y
```



### z

```python
z
```



