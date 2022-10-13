import sys
from functools import lru_cache
from pathlib import Path

from seagulls.assets import AssetManager
from seagulls.seagulls_cli import (
    SeagullsAppDiContainer,
    SeagullsCliApplication,
    SeagullsRuntimeClient
)

from ._cli_command import GameCliCommand
from ._cli_plugin import WhereInTheWorldDemoCliPlugin


class WhereInTheWorldDemoDiContainer:
    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication):
        self._application = application

    @lru_cache()
    def plugin(self) -> WhereInTheWorldDemoCliPlugin:
        return WhereInTheWorldDemoCliPlugin(
            application=self._application,
            command=self._command(),
        )

    @lru_cache()
    def _command(self) -> GameCliCommand:
        return GameCliCommand(asset_manager=self._asset_manager())

    @lru_cache()
    def _asset_manager(self) -> AssetManager:
        return AssetManager(assets_path=self._find_assets_path())

    @lru_cache()
    def _find_assets_path(self) -> Path:
        if self._runtime_client().is_bundled():
            return Path(f"{getattr(sys, '_MEIPASS')}/seagulls_assets")

        container_dir_path = Path(__file__).parent
        parts = str(container_dir_path.resolve()).split("/site-packages/")
        if len(parts) == 2:
            return Path(parts[0]) / "site-packages/seagulls_assets"

        return Path("seagulls_assets")

    @lru_cache()
    def _runtime_client(self) -> SeagullsRuntimeClient:
        return self._seagulls_app_container().runtime_client()

    @lru_cache()
    def _seagulls_app_container(self) -> SeagullsAppDiContainer:
        return self._application.get_container(SeagullsAppDiContainer)
