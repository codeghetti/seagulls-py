from argparse import ArgumentParser
from typing import Iterable, Tuple, TypeAlias

from seagulls.cat_demos.engine.v2.components._client_containers import (
    GameClientProvider,
    Tco_GameClientType,
)
from seagulls.cat_demos.engine.v2.components._entities import GameClientId
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp
from seagulls.cli import ICliCommand

ComponentProviderCollection: TypeAlias = Iterable[
    Tuple[GameClientId[Tco_GameClientType], GameClientProvider[Tco_GameClientType]]
]


class GameCliCommand(ICliCommand):
    _app: SeagullsApp
    _app_providers_factory: GameClientProvider[ComponentProviderCollection]

    def __init__(
        self,
        app: SeagullsApp,
        app_providers_factory: GameClientProvider[ComponentProviderCollection],
    ) -> None:
        self._app = app
        self._app_providers_factory = app_providers_factory

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        try:
            self._run()
        except KeyboardInterrupt:
            pass

    def _run(self) -> None:
        self._app.run(*self._app_providers_factory())
