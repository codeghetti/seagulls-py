import logging
from functools import lru_cache
from typing import Any, Callable, Dict, List, Type

from seagulls.app import (
    IPluggableSeagullsApplication,
    ISeagullsApplication,
    ISeagullsApplicationPlugin,
    ISeagullsPluginClient,
    PluginType
)
from seagulls.cli import CliRequest
from seagulls.eventing import EventCallbackType, EventType, IDispatchEvents

from ._container_repository import DiContainerRepository, ObjectType
from ._logging_client import LoggingClient

logger = logging.getLogger(__name__)


class PostPluginRegistrationEvent:
    pass


class SeagullsCliApplication(
        ISeagullsApplication,
        IPluggableSeagullsApplication,
        IDispatchEvents):

    _container_repository: DiContainerRepository
    _plugin_client: ISeagullsPluginClient
    _logging_client: LoggingClient
    _request: CliRequest

    _plugins: Dict[Any, Any]
    _callbacks: Dict[Any, List[Any]]

    def __init__(
            self,
            container_repository: DiContainerRepository,
            plugin_client: ISeagullsPluginClient,
            logging_client: LoggingClient,
            request: CliRequest):
        self._container_repository = container_repository
        self._plugin_client = plugin_client
        self._logging_client = logging_client
        self._request = request

        self._plugins = {}
        self._callbacks = {}

    def execute(self) -> None:
        self._plugin_client.register_plugins(self)
        self.trigger_event(PostPluginRegistrationEvent())
        self._request.execute(event_dispatcher=self)

    def register_container(self, key: Type[ObjectType], container: ObjectType) -> None:
        self._container_repository.register(key, container)

    def get_container(self, key: Type[ObjectType]) -> ObjectType:
        return self._container_repository.get(key)

    def register_callback(
            self,
            event_type: Type[EventType],
            callback: EventCallbackType) -> None:
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []

        self._callbacks[event_type].append(callback)

    def trigger_event(self, event: EventType) -> None:
        for callback in self._callbacks.get(type(event), []):
            callback(event)

    def register_plugin(self, plugin: ISeagullsApplicationPlugin) -> None:
        if type(plugin) in self._plugins:
            raise DuplicatePluginError(plugin)

        self._plugins[type(plugin)] = plugin
        plugin.on_registration()

    @lru_cache()
    def get_plugin(self, plugin_type: Type[PluginType]) -> PluginType:  # type: ignore
        return self._plugins[plugin_type]

    def _apply_to_plugins(self, callback: Callable[[PluginType], None]) -> None:
        for plugin in self._plugins.values():
            callback(plugin)


class DuplicatePluginError(RuntimeError):
    plugin: ISeagullsApplicationPlugin

    def __init__(self, plugin: ISeagullsApplicationPlugin):
        super().__init__(f"Duplicate plugin registration detected: {type(plugin)}")
        self.plugin = plugin
