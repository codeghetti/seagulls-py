from dataclasses import dataclass

from seagulls.cat_demos.engine.v2.input._eventing import InputEvent
from seagulls.cat_demos.engine.v2.position._position_component import Vector


class QuitGameEvent:
    pass


@dataclass(frozen=True)
class PlayerMoveEvent:
    direction: Vector


class GameInputs:
    """
    We want to be able to reference all our game input ids in a simple way. This class allows us to
    reference things as GameInputs.QUIT. The typing information here allows IDEs to know that the
    GameInputs.QUIT event has a payload of type QuitGameEvent.

    Drawbacks:
    The main issue I have here is that this class is not immutable. We can make it immutable by
    using something like a NamedTuple. But the code to define it that way would be considerably
    more confusing, which I opted out of. The other issue is that python doesn't have constants. So
    even if we used a NamedTuple, the assignment of the NamedTuple to a variable would still be
    mutable.

    The is another minor issue in that the definition of these values is quite verbose. Pycharm
    didn't seem to infer the type of these variables from the assignment of the values. So I had
    to copy the type signature to both sides of the assignment.
    """
    QUIT = InputEvent[QuitGameEvent]("quit-game")
    MOVE = InputEvent[PlayerMoveEvent]("player-move")
    MOVE_UP = InputEvent[PlayerMoveEvent]("player-move[up]")
    MOVE_DOWN = InputEvent[PlayerMoveEvent]("player-move[down]")
    MOVE_LEFT = InputEvent[PlayerMoveEvent]("player-move[left]")
    MOVE_RIGHT = InputEvent[PlayerMoveEvent]("player-move[right]")
