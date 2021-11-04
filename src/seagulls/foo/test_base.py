class SomeBaseClass:
    """
    Documentation for `SomeBaseClass`.
    """

    base_property: str
    """
    Documentation for `SomeBaseClass.base_property`.
    """

    base_property_with_default: str = "hello"
    """
    Documentation for `SomeBaseClass.base_property_with_default`.
    """

    def __init__(self, arg1: str):
        """
        This is the documentation for `SomeBaseClass.__init__()`.

        Args:
            arg1: The docs for arg1 arg in `SomeBaseClass.__init__()`.
        """
        super().__init__()
        pass

    def some_base_method(self, arg1: int, *args, **kwargs) -> None:
        """
        This is the documentation for `SomeBaseClass.some_base_method()`.
        """
        pass


class AnotherBaseClass(SomeBaseClass):
    """
    Documentation for `AnotherBaseClass`.
    """

    another_property: str
    """
    Documentation for `AnotherBaseClass.another_property`.
    """

    def another_base_method(self, arg1: int, *args, **kwargs) -> None:
        """
        This is the documentation for `AnotherBaseClass.another_base_method()`.
        """
        pass
