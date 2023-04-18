from argparse import ArgumentParser
from typing import Iterable, Tuple, TypeAlias

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId, GameComponentProvider, \
    GameComponentType
from seagulls.cat_demos.engine.v2.components._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp
from seagulls.cli import ICliCommand

ComponentProviderCollection: TypeAlias = Iterable[
    Tuple[GameComponentId[GameComponentType], GameComponentProvider[GameComponentType]]
]


class GameCliCommand(ICliCommand):

    _app: SeagullsApp
    _app_providers_factory: ServiceProvider[ComponentProviderCollection]

    def __init__(self, app: SeagullsApp, app_providers_factory: ServiceProvider[ComponentProviderCollection]) -> None:
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
