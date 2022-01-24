import os
from functools import lru_cache
from pathlib import Path
import sys
from typing import Tuple

from ._application import SeagullsCliApplication
from seagulls.cli import CliRequest
from ._container_repository import DiContainerRepository
from seagulls.cli import RequestEnvironment
from ._logging_client import LoggingClient
from seagulls.app import SeagullsEntryPointsPluginsClient


class SeagullsAppDiContainer:

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
            file=Path(sys.argv[0]).resolve(),
            args=tuple(sys.argv[1:]),
            env=RequestEnvironment(env_tuple),
        )

    @lru_cache()
    def logging_client(self) -> LoggingClient:
        return LoggingClient(verbosity=2)

    @lru_cache()
    def _plugin_client(self) -> SeagullsEntryPointsPluginsClient:
        return SeagullsEntryPointsPluginsClient("seagulls.plugins")

    @lru_cache()
    def _container_registry(self) -> DiContainerRepository:
        instance = DiContainerRepository()
        instance.register(SeagullsAppDiContainer, self)
        return instance
