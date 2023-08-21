from functools import lru_cache

from seagulls.cat_demos.app._cli_command import GameCliCommand
from seagulls.cat_demos.app._cli_plugin import CatDemosCliPlugin
from seagulls.cat_demos.app._component_providers import (
    CatDemosAppSettings,
    CatDemosComponentProviders,
    ProcessType
)
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp
from seagulls.seagulls_cli import SeagullsCliApplication


class CatDemosDiContainer:
    _application: SeagullsCliApplication

    # def __init__(self, application: SeagullsCliApplication) -> None:
    #     self._application = application

    @lru_cache()
    def plugin(self) -> CatDemosCliPlugin:
        return CatDemosCliPlugin(
            application=self._application,
            launch_command=self._launch_command(),
            dev_command=self._dev_command(),
        )

    @lru_cache()
    def _launch_command(self) -> GameCliCommand:
        return GameCliCommand(
            app=self.app(), app_providers_factory=self.standalone_providers()
        )

    @lru_cache()
    def _dev_command(self) -> GameCliCommand:
        return GameCliCommand(
            app=self.app(), app_providers_factory=self._client_providers()
        )

    @lru_cache()
    def standalone_providers(self) -> CatDemosComponentProviders:
        return CatDemosComponentProviders(
            app=self.app(),
            settings=lambda: CatDemosAppSettings(
                process_type=ProcessType.STANDALONE,
            ),
        )

    @lru_cache()
    def _client_providers(self) -> CatDemosComponentProviders:
        return CatDemosComponentProviders(
            app=self.app(),
            settings=lambda: CatDemosAppSettings(
                process_type=ProcessType.CLIENT,
            ),
        )

    @lru_cache()
    def app(self) -> SeagullsApp:
        return SeagullsApp()
