from functools import lru_cache

from seagulls.cat_demos.app._cli_command import GameCliCommand
from seagulls.cat_demos.app._cli_plugin import CatDemosCliPlugin
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp
from seagulls.seagulls_cli import SeagullsCliApplication


class CatDemosDiContainer:

    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication) -> None:
        self._application = application

    @lru_cache()
    def plugin(self) -> CatDemosCliPlugin:
        return CatDemosCliPlugin(
            application=self._application,
            command=self._command(),
        )

    @lru_cache()
    def _command(self) -> GameCliCommand:
        return GameCliCommand(
            app=self._app(),
        )

    @lru_cache()
    def _app(self) -> SeagullsApp:
        return SeagullsApp()
