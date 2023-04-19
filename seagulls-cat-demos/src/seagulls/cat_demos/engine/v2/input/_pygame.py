import logging
from functools import lru_cache
from typing import NamedTuple

import pygame

from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEvent, GameEventDispatcher, GameEventId
from seagulls.cat_demos.engine.v2.position._point import Point, Position

logger = logging.getLogger(__name__)


class PygameKeyboardEvent(NamedTuple):
    type: int
    key: int


class PygameMouseMotionEvent(NamedTuple):
    position: Position
    previous_position: Position

    @lru_cache()
    def movement(self) -> Point:
        return self.position - self.previous_position


class PygameEvents:
    KEYBOARD = GameEventId[PygameKeyboardEvent](name='seagulls:pygame-input.keyboard')
    MOUSE_MOTION = GameEventId[PygameMouseMotionEvent](name='seagulls:pygame-input.mouse-motion')
    QUIT = GameEventId[None](name='seagulls:pygame-input.quit')

    @staticmethod
    def key(x: int) -> GameEventId[PygameKeyboardEvent]:
        return GameEventId[PygameKeyboardEvent](name=f'seagulls:pygame-input.keyboard:{x}')

    @staticmethod
    def key_pressed(x: int) -> GameEventId[PygameKeyboardEvent]:
        return GameEventId[PygameKeyboardEvent](name=f'seagulls:pygame-input.keyboard:{x}:pressed')

    @staticmethod
    def key_released(x: int) -> GameEventId[PygameKeyboardEvent]:
        return GameEventId[PygameKeyboardEvent](name=f'seagulls:pygame-input.keyboard:{x}:released')


"""
What if game events were executables and observers decided between being notified `before()` or `after()` events? This
should allow us to avoid event dispatcher code being messy, requiring us to sprinkle `trigger()` before and after any
interesting line of code. Defining the event executables feels more natural because the execution of the business logic
is explained in a format of an event happening, which is reasonable prose even in the absense of an event dispatcher.

"We want to be able to move players."
Might be the reason we create the ability to execute `player.move(Direction(x=2, y=1))` somewhere in our application.

"We want to be able to have player objects say something"
`player.say(Utterance("hello, there!"))  # typing Utterance makes my left hand kinda hurt`

"No we don't care what the player says"
`player.speak()`

"We want the camera object to follow the player"
`camera.move(Direction(???))`

"We want the camera movement to be smoother when the player changes position"
"We want the camera to focus about 200px in front of the player position, accounting for player direction"
"We want player objects to behave as rigidbodies and stand on platforms"
"We want platform objects to be destroyed when the player's head touches the bottom of the platform"
"Some platforms should toss a coin in the air when destroyed"

```python
event_dispatcher = EventDispatcher()

# defining the unit of business logic looks like registering a callback and picking an event id
# the event id is bound to the class type of the event payload
# the old eventing behavior can be simulated by defining an event with a no-op callback (only observers run) 
event_dispatcher.define(EventId[Direction]("move-player"), lambda payload: print(f"moving player amount: {payload}"))

# triggering an event is the same as calling a method with a payload argument
event_dispatcher.trigger(EventId[Position]("move-player"), Direction(x=2, y=1))
# with a simple wrapper, we can even re-create the exact same API
player.move = partial(event_dispatcher.trigger, EventId[Position]("move-player"))

# observers register to run before or after an event id
event_dispatcher.before(EventId[Position]("move-player"), lambda: print("we're about to move the player"))
event_dispatcher.after(EventId[Position]("move-player"), lambda: print("we finished moving the player"))

# observers don't get passed the payload because nested events can cause multiple payloads to be "active"
# observers can use the dispatcher to fetch payloads by event id
position = event_dispatcher.payload(EventId[Position]("move-player"))

# if there are two or more active payloads for a given event id, the most recently activated is returned
# but we can still get to the other payloads by getting them all
player_moves = event_dispatcher.payloads(EventId[Position]("move-player"))

# retrieving all payloads without filtering by event id is not possible because the returned value would have no type
# but it might be useful to use the event id to match patterns, maybe with package-like event names
moves = event_dispatcher.find_payloads(EventId[Position]("move.*"))

# what about being able to make additional payloads available while an event id is active?
# can we implement collisions like this?
# transactions that roll back some of the movement operations?
# how do I calculate the direction and position of the collisions?
"""


class PygameKeyboardInputPublisher:

    _event_dispatcher: GameEventDispatcher

    def __init__(self, event_dispatcher: GameEventDispatcher) -> None:
        self._event_dispatcher = event_dispatcher

    def tick(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                self._event_dispatcher.trigger(GameEvent(
                    PygameEvents.KEYBOARD,
                    PygameKeyboardEvent(type=event.type, key=event.key),
                ))
                self._event_dispatcher.trigger(GameEvent(
                    PygameEvents.key(event.key),
                    PygameKeyboardEvent(type=event.type, key=event.key),
                ))
            if event.type == pygame.KEYDOWN:
                self._event_dispatcher.trigger(GameEvent(
                    PygameEvents.key_pressed(event.key),
                    PygameKeyboardEvent(type=event.type, key=event.key),
                ))
            if event.type == pygame.KEYUP:
                self._event_dispatcher.trigger(GameEvent(
                    PygameEvents.key_released(event.key),
                    PygameKeyboardEvent(type=event.type, key=event.key),
                ))
            if event.type == pygame.QUIT:
                self._event_dispatcher.trigger(GameEvent(PygameEvents.QUIT, None))
            if event.type == pygame.MOUSEMOTION:
                self._event_dispatcher.trigger(
                    GameEvent(PygameEvents.MOUSE_MOTION, PygameMouseMotionEvent(
                        position=Position(*event.pos),
                        previous_position=Position(event.pos[0] + event.rel[0], event.pos[1] + event.rel[1])
                    ))
                )
            else:
                logger.debug(f"unknown pygame event detected: {event}")
