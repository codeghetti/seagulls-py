---
title: "seagulls.devtools"
---


# [seagulls](../seagulls).devtools


??? note "View Source"
    ```python
        from ._cli_entry_point import DevtoolsCliPluginEntryPoint

        __all__ = [
            "DevtoolsCliPluginEntryPoint",
        ]

    ```

## DevtoolsCliPluginEntryPoint

```python
class DevtoolsCliPluginEntryPoint(seagulls.app._plugin_interfaces.ISeagullsApplicationPluginRegistrant[seagulls.seagulls_cli._application.SeagullsCliApplication]):
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
        class DevtoolsCliPluginEntryPoint(
                ISeagullsApplicationPluginRegistrant[SeagullsCliApplication]):

            @staticmethod
            def register_plugins(application: SeagullsCliApplication) -> None:
                di_container = SeagullsDevtoolsDiContainer(application=application)
                application.register_plugin(di_container.plugin())

    ```


### register_plugins()

```python
@staticmethod
def register_plugins(
    application: seagulls.seagulls_cli._application.SeagullsCliApplication
) -> None:
```

Called at the start of the process for plugin devs to register their plugins in the app.

??? note "View Source"
    ```python
            @staticmethod
            def register_plugins(application: SeagullsCliApplication) -> None:
                di_container = SeagullsDevtoolsDiContainer(application=application)
                application.register_plugin(di_container.plugin())

    ```


### Inherited Members

**taken from:** seagulls.app._plugin_interfaces:ISeagullsApplicationPluginRegistrant

- `#!python ISeagullsApplicationPluginRegistrant(*args, **kwargs)`
