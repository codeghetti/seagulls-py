---
title: "seagulls.seagulls_cli"
---


# [seagulls](../seagulls).seagulls_cli


??? note "View Source"
    ```python
        from ._application import SeagullsCliApplication
        from ._entry_point import main

        __all__ = [
            "SeagullsCliApplication",
            "main",
        ]

    ```

## SeagullsCliApplication

```python
class SeagullsCliApplication(seagulls.app._app_interfaces.ISeagullsApplicationseagulls.app._plugin_interfaces.IPluggableSeagullsApplicationseagulls.eventing._interfaces.IDispatchEvents):
```

Base class for protocol classes.

Protocol classes are defined as::

    class Proto(Protocol):
        def meth(self) -&gt; int:
            ...

Such classes are primarily used with static type checkers that recognize
structural subtyping (static duck-typing), for example::

    class C:
        def meth(self) -&gt; int:
            return 0

    def func(x: Proto) -&gt; int:
        return x.meth()

    func(C())  # Passes static type check

See PEP 544 for details. Protocol classes decorated with
@typing.runtime_checkable act as simple-minded runtime protocols that check
only the presence of given attributes, ignoring their type signatures.
Protocol classes can be generic, they are defined as::

    class GenProto(Protocol[T]):
        def meth(self) -&gt; T:
            ...

??? note "View Source"
    ```python
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

    ```


### SeagullsCliApplication()

```python
SeagullsCliApplication(
    container_repository: seagulls.seagulls_cli._container_repository.DiContainerRepository,
    plugin_client: seagulls.app._plugin_interfaces.ISeagullsPluginClient,
    logging_client: seagulls.seagulls_cli._logging_client.LoggingClient,
    request: seagulls.cli._request.CliRequest
):
```


??? note "View Source"
    ```python
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

    ```


### execute()

```python
def execute(self) -> None:
```


??? note "View Source"
    ```python
            def execute(self) -> None:
                self._plugin_client.register_plugins(self)
                self.trigger_event(PostPluginRegistrationEvent())
                self._request.execute(event_dispatcher=self)

    ```


### register_container()

```python
def register_container(self, key: Type[~ObjectType], container: ~ObjectType) -> None:
```


??? note "View Source"
    ```python
            def register_container(self, key: Type[ObjectType], container: ObjectType) -> None:
                self._container_repository.register(key, container)

    ```


### get_container()

```python
def get_container(self, key: Type[~ObjectType]) -> ~ObjectType:
```


??? note "View Source"
    ```python
            def get_container(self, key: Type[ObjectType]) -> ObjectType:
                return self._container_repository.get(key)

    ```


### register_callback()

```python
def register_callback(
    self,
    event_type: Type[~EventType],
    callback: Callable[[~EventType], NoneType]
) -> None:
```


??? note "View Source"
    ```python
            def register_callback(
                    self,
                    event_type: Type[EventType],
                    callback: EventCallbackType) -> None:
                if event_type not in self._callbacks:
                    self._callbacks[event_type] = []

                self._callbacks[event_type].append(callback)

    ```


### trigger_event()

```python
def trigger_event(self, event: ~EventType) -> None:
```


??? note "View Source"
    ```python
            def trigger_event(self, event: EventType) -> None:
                for callback in self._callbacks.get(type(event), []):
                    callback(event)

    ```


### register_plugin()

```python
def register_plugin(
    self,
    plugin: seagulls.app._plugin_interfaces.ISeagullsApplicationPlugin
) -> None:
```


??? note "View Source"
    ```python
            def register_plugin(self, plugin: ISeagullsApplicationPlugin) -> None:
                if type(plugin) in self._plugins:
                    raise DuplicatePluginError(plugin)

                self._plugins[type(plugin)] = plugin
                plugin.on_registration()

    ```


### get_plugin()

```python
@lru_cache()
def get_plugin(self, plugin_type: Type[~PluginType]) -> ~PluginType:
```


??? note "View Source"
    ```python
            @lru_cache()
            def get_plugin(self, plugin_type: Type[PluginType]) -> PluginType:  # type: ignore
                return self._plugins[plugin_type]

    ```


## main()

```python
def main():
```


??? note "View Source"
    ```python
        def main():
            di_container = SeagullsAppDiContainer()
            app = di_container.application()
            app.execute()

    ```


