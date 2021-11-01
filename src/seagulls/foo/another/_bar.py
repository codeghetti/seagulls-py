"""
Example submodule being exposed through `seagulls.foo.another`.
"""


class SomeFooBar:
    """Blah Blah, SomeFooBar."""

    thing: int = 5
    """The thing thing."""

    def do_it(self, arg: int) -> None:
        """
        Does the thing.

        Args:
            arg: number of times to do the thing
        """
