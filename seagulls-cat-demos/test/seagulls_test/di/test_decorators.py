class SomeClient:
    pass


class SomeContainer:

    def some_client(self) -> SomeClient:
        return SomeClient()


class TestDecorators:

    def test_basics(self) -> None:
        container = SomeContainer()
        container.some_client()
