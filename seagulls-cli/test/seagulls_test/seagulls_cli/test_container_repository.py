import pytest

from seagulls.seagulls_cli._container_repository import (
    DiContainerNotFoundError,
    DiContainerRepository,
    DuplicateDiContainerKeyError
)


class Something:
    pass


class AnotherThing:
    pass


class TestDiContainerRepository:
    _instance: DiContainerRepository

    def setup(self) -> None:
        self._instance = DiContainerRepository()

    def test_basics(self) -> None:
        thing = Something()
        self._instance.register(Something, thing)

        assert self._instance.get(Something) == thing

    def test_missing_container(self) -> None:
        with pytest.raises(DiContainerNotFoundError):
            self._instance.get(Something)

    def test_duplicate_container(self) -> None:
        thing1 = Something()
        thing2 = AnotherThing()
        thing3 = Something()

        self._instance.register(Something, thing1)
        self._instance.register(AnotherThing, thing2)

        with pytest.raises(DuplicateDiContainerKeyError):
            self._instance.register(Something, thing3)
