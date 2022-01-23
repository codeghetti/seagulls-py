---
title: "seagulls.app"
---


# [seagulls](../seagulls).app


??? note "View Source"
    ```python
        from ._app_interfaces import ISeagullsApplication
        from ._plugin_client import SeagullsEntryPointsPluginsClient
        from ._plugin_interfaces import (
            ApplicationType,
            PluginType,
            ISeagullsApplicationPlugin,
            IPluggableSeagullsApplication,
            ISeagullsPluginClient,
            ISeagullsApplicationPluginRegistrant,
        )
        from ._plugin_exceptions import DuplicatePluginError

        __all__ = [
            # App
            "ISeagullsApplication",
            # Plugin Client
            "SeagullsEntryPointsPluginsClient",
            # App Plugins
            "ApplicationType",
            "PluginType",
            "ISeagullsApplicationPlugin",
            "IPluggableSeagullsApplication",
            "ISeagullsPluginClient",
            "ISeagullsApplicationPluginRegistrant",
            # Exceptions
            "DuplicatePluginError",
        ]

    ```

## ISeagullsApplication

```python
class ISeagullsApplication(typing.Protocol):
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
        class ISeagullsApplication(Protocol):

            @abstractmethod
            def execute(self) -> None: ...

    ```


### execute()

```python
@abstractmethod
def execute(self) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def execute(self) -> None: ...

    ```


## SeagullsEntryPointsPluginsClient

```python
class SeagullsEntryPointsPluginsClient(seagulls.app._plugin_interfaces.ISeagullsPluginClient):
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
        class SeagullsEntryPointsPluginsClient(ISeagullsPluginClient):

            _entrypoint_name: str

            def __init__(self, entrypoint_name: str):
                self._entrypoint_name = entrypoint_name

            def register_plugins(self, application: ApplicationType) -> None:
                plugins = entry_points(group=self._entrypoint_name)
                for plugin in plugins:
                    plugin_ref: Type[ISeagullsApplicationPluginRegistrant] = plugin.load()
                    if not issubclass(plugin_ref, ISeagullsApplicationPluginRegistrant):
                        raise InvalidPluginError(plugin)

                    plugin_ref.register_plugins(application)  # type: ignore

    ```


### SeagullsEntryPointsPluginsClient()

```python
SeagullsEntryPointsPluginsClient(entrypoint_name: str):
```


??? note "View Source"
    ```python
            def __init__(self, entrypoint_name: str):
                self._entrypoint_name = entrypoint_name

    ```


### register_plugins()

```python
def register_plugins(self, application: -ApplicationType) -> None:
```

Find all plugins and let them register plugins to the running application.

??? note "View Source"
    ```python
            def register_plugins(self, application: ApplicationType) -> None:
                plugins = entry_points(group=self._entrypoint_name)
                for plugin in plugins:
                    plugin_ref: Type[ISeagullsApplicationPluginRegistrant] = plugin.load()
                    if not issubclass(plugin_ref, ISeagullsApplicationPluginRegistrant):
                        raise InvalidPluginError(plugin)

                    plugin_ref.register_plugins(application)  # type: ignore

    ```


## ApplicationType

```python
ApplicationType = -ApplicationType
```



## PluginType

```python
PluginType = ~PluginType
```



## ISeagullsApplicationPlugin

```python
class ISeagullsApplicationPlugin(typing.Protocol):
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
        class ISeagullsApplicationPlugin(Protocol):

            @abstractmethod
            def on_registration(self) -> None:
                """
                Called when the plugin is first registered with the application.
                """

    ```


### on_registration()

```python
@abstractmethod
def on_registration(self) -> None:
```

Called when the plugin is first registered with the application.

??? note "View Source"
    ```python
            @abstractmethod
            def on_registration(self) -> None:
                """
                Called when the plugin is first registered with the application.
                """

    ```


## IPluggableSeagullsApplication

```python
class IPluggableSeagullsApplication(typing.Protocol):
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
        class IPluggableSeagullsApplication(Protocol):

            @abstractmethod
            def register_plugin(self, plugin: ISeagullsApplicationPlugin) -> None: ...

            @abstractmethod
            def get_plugin(self, plugin: Type[PluginType]) -> PluginType: ...

    ```


### register_plugin()

```python
@abstractmethod
def register_plugin(
    self,
    plugin: seagulls.app._plugin_interfaces.ISeagullsApplicationPlugin
) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def register_plugin(self, plugin: ISeagullsApplicationPlugin) -> None: ...

    ```


### get_plugin()

```python
@abstractmethod
def get_plugin(self, plugin: Type[~PluginType]) -> ~PluginType:
```


??? note "View Source"
    ```python
            @abstractmethod
            def get_plugin(self, plugin: Type[PluginType]) -> PluginType: ...

    ```


## ISeagullsPluginClient

```python
class ISeagullsPluginClient(typing.Protocol):
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
        class ISeagullsPluginClient(Protocol):

            @abstractmethod
            def register_plugins(self, application: ApplicationType) -> None:
                """
                Find all plugins and let them register plugins to the running application.
                """

    ```


### register_plugins()

```python
@abstractmethod
def register_plugins(self, application: -ApplicationType) -> None:
```

Find all plugins and let them register plugins to the running application.

??? note "View Source"
    ```python
            @abstractmethod
            def register_plugins(self, application: ApplicationType) -> None:
                """
                Find all plugins and let them register plugins to the running application.
                """

    ```


## ISeagullsApplicationPluginRegistrant

```python
@runtime_checkable
class ISeagullsApplicationPluginRegistrant(typing.Protocol[-ApplicationType]):
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
        @runtime_checkable
        class ISeagullsApplicationPluginRegistrant(Protocol[ApplicationType]):

            @staticmethod
            @abstractmethod
            def register_plugins(application: ApplicationType) -> None:
                """
                Called at the start of the process for plugin devs to register their plugins in the app.
                """

    ```


### register_plugins()

```python
@staticmethod
@abstractmethod
def register_plugins(application: -ApplicationType) -> None:
```

Called at the start of the process for plugin devs to register their plugins in the app.

??? note "View Source"
    ```python
            @staticmethod
            @abstractmethod
            def register_plugins(application: ApplicationType) -> None:
                """
                Called at the start of the process for plugin devs to register their plugins in the app.
                """

    ```


## DuplicatePluginError

```python
class DuplicatePluginError(builtins.RuntimeError):
```

Unspecified run-time error.

??? note "View Source"
    ```python
        class DuplicatePluginError(RuntimeError):
            plugin: ISeagullsApplicationPlugin

            def __init__(self, plugin: ISeagullsApplicationPlugin):
                super().__init__(f"Duplicate plugin registration detected: {type(plugin)}")
                self.plugin = plugin

    ```


### DuplicatePluginError()

```python
DuplicatePluginError(plugin: seagulls.app._plugin_interfaces.ISeagullsApplicationPlugin):
```


??? note "View Source"
    ```python
            def __init__(self, plugin: ISeagullsApplicationPlugin):
                super().__init__(f"Duplicate plugin registration detected: {type(plugin)}")
                self.plugin = plugin

    ```


### Inherited Members

**taken from:** builtins:BaseException

- `#!python with_traceback()`
- `#!python args`
