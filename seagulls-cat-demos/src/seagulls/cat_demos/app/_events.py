class AppEvents:
    """
    We want to be able to reference all our game input ids in a simple way. This class allows us to
    reference things as AppEvents.QUIT. The typing information here allows IDEs to know that the
    AppEvents.QUIT event has a payload of type QuitGameEvent.

    Drawbacks:
    The main issue I have here is that this class is not immutable. We can make it immutable by
    using something like a NamedTuple. But the code to define it that way would be considerably
    more confusing, which I opted out of. The other issue is that python doesn't have constants. So
    even if we used a NamedTuple, the assignment of the NamedTuple to a variable would still be
    mutable.
    """

    # QUIT = GameEventId[QuitGameConfig]("quit-game")
