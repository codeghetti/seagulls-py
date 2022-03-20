import os
from functools import lru_cache
from pathlib import Path
from typing import Tuple, cast

from importlib_metadata import entry_points
from seagulls.app import (
    EntryPointsCallback,
    SeagullsEntryPointsPluginsClient,
    SeagullsEntryPointsPluginSource
)
from seagulls.cli import CliRequest, RequestEnvironment

from ._application import SeagullsCliApplication
from ._container_repository import DiContainerRepository
from ._logging_client import LoggingClient


class SeagullsAppDiContainer:

    _argv: Tuple[str, ...]

    def __init__(self, argv: Tuple[str, ...]):
        self._argv = argv

    @lru_cache()
    def application(self) -> SeagullsCliApplication:
        return SeagullsCliApplication(
            container_repository=self._container_registry(),
            plugin_client=self._plugin_client(),
            logging_client=self.logging_client(),
            request=self._request(),
        )

    @lru_cache()
    def _request(self) -> CliRequest:
        env_tuple: Tuple[Tuple[str, str], ...] = tuple(os.environ.items())  # type: ignore
        return CliRequest(
            file=Path(self._argv[0]).resolve(),
            args=tuple(self._argv[1:]),
            env=RequestEnvironment(env_tuple),
        )

    @lru_cache()
    def logging_client(self) -> LoggingClient:
        return LoggingClient(verbosity=2)

    @lru_cache()
    def _plugin_client(self) -> SeagullsEntryPointsPluginsClient:
        callback = cast(EntryPointsCallback, entry_points)
        return SeagullsEntryPointsPluginsClient(
            entrypoint_source=SeagullsEntryPointsPluginSource(callback),
            entrypoint_name="seagulls.plugins",
        )

    @lru_cache()
    def _container_registry(self) -> DiContainerRepository:
        instance = DiContainerRepository()
        instance.register(SeagullsAppDiContainer, self)
        return instance
