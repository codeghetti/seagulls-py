"""
This is the comment for the module.
"""
from functools import lru_cache
from typing import Optional

some_variable = 10
"""
Just commenting about `some_variable`.
"""


def some_function(arg1: str, arg2: int) -> Optional[str]:
    """
    This is the documentation for `some_function`.

    Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.
    Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.
    Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.

    Args:
        arg1: docs for `some_function()` arg arg1.
        arg2: docs for `some_function()` arg arg2.

    Returns:
        docs for `some_function()` return value
    """
    return "my value"


class SomeClass(str):
    """
    Documentation for `SomeClass`.
    """

    some_property: str
    """
    Documentation for `SomeClass.some_property`.
    """

    def __init__(self, arg1: str):
        """
        This is the documentation for `SomeClass.__init__()`.

        Args:
            arg1: The docs for arg1 arg in `SomeClass.__init__()`.
        """
        super().__init__()
        pass

    @lru_cache()
    def some_method(self) -> None:
        """
        This is the documentation for `SomeClass.some_method()`.
        """
        pass
