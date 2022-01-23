---
title: "seagulls.cli"
---


# [seagulls](../seagulls).cli


??? note "View Source"
    ```python
        from ._request import (
            CliRequest,
            ICliCommand,
            RequestEnvironment,
            CliRequestRegistrationEvent,
        )

        __all__ = [
            "CliRequest",
            "ICliCommand",
            "RequestEnvironment",
            "CliRequestRegistrationEvent",
        ]

    ```

## CliRequest

```python
class CliRequest:
```


??? note "View Source"
    ```python
        class CliRequest:

            _file: Path
            _args: Tuple[str, ...]
            _env: RequestEnvironment

            def __init__(
                    self,
                    file: Path,
                    args: Tuple[str, ...],
                    env: RequestEnvironment):
                self._file = file
                self._args = args
                self._env = env

            def execute(self, event_dispatcher: IDispatchEvents) -> None:
                # Build the CLI Command Interface
                parser = ArgumentParser(
                    description="Seagulls CLI Command",
                )

                event = CliRequestRegistrationEvent(parser)
                event_dispatcher.trigger_event(event)

                def default_execute() -> None:
                    parser.print_help()

                parser.set_defaults(cmd=default_execute)

                args = parser.parse_args(self._args)
                args.cmd()

    ```


### CliRequest()

```python
CliRequest(
    file: pathlib.Path,
    args: Tuple[str, ...],
    env: seagulls.cli._request.RequestEnvironment
):
```


??? note "View Source"
    ```python
            def __init__(
                    self,
                    file: Path,
                    args: Tuple[str, ...],
                    env: RequestEnvironment):
                self._file = file
                self._args = args
                self._env = env

    ```


### execute()

```python
def execute(
    self,
    event_dispatcher: seagulls.eventing._interfaces.IDispatchEvents
) -> None:
```


??? note "View Source"
    ```python
            def execute(self, event_dispatcher: IDispatchEvents) -> None:
                # Build the CLI Command Interface
                parser = ArgumentParser(
                    description="Seagulls CLI Command",
                )

                event = CliRequestRegistrationEvent(parser)
                event_dispatcher.trigger_event(event)

                def default_execute() -> None:
                    parser.print_help()

                parser.set_defaults(cmd=default_execute)

                args = parser.parse_args(self._args)
                args.cmd()

    ```


## ICliCommand

```python
class ICliCommand(typing.Protocol):
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
        class ICliCommand(Protocol):

            @abstractmethod
            def configure_parser(self, parser: ArgumentParser) -> None: ...

            @abstractmethod
            def execute(self) -> None: ...

    ```


### configure_parser()

```python
@abstractmethod
def configure_parser(self, parser: argparse.ArgumentParser) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def configure_parser(self, parser: ArgumentParser) -> None: ...

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


## RequestEnvironment

```python
class RequestEnvironment:
```


??? note "View Source"
    ```python
        class RequestEnvironment:

            _values: Dict[str, str]

            def __init__(self, values: Tuple[EnvironmentTuple, ...]):
                self._values = {k: v for k, v in values}

            def get(self, name: str, default: str = None) -> Optional[str]:
                return self._values.get(name, default)

            def as_dict(self) -> Dict[str, str]:
                return self._values.copy()

    ```


### RequestEnvironment()

```python
RequestEnvironment(values: Tuple[Tuple[str, str], ...]):
```


??? note "View Source"
    ```python
            def __init__(self, values: Tuple[EnvironmentTuple, ...]):
                self._values = {k: v for k, v in values}

    ```


### get()

```python
def get(self, name: str, default: str = None) -> Optional[str]:
```


??? note "View Source"
    ```python
            def get(self, name: str, default: str = None) -> Optional[str]:
                return self._values.get(name, default)

    ```


### as_dict()

```python
def as_dict(self) -> Dict[str, str]:
```


??? note "View Source"
    ```python
            def as_dict(self) -> Dict[str, str]:
                return self._values.copy()

    ```


## CliRequestRegistrationEvent

```python
class CliRequestRegistrationEvent:
```


??? note "View Source"
    ```python
        class CliRequestRegistrationEvent:

            _parser: ArgumentParser

            def __init__(self, parser: ArgumentParser):
                self._parser = parser

            def register_command(self, name: str, command: ICliCommand) -> None:
                def callback() -> None:
                    command.execute()
                subparser = self._get_subparsers().add_parser(name=name)
                command.configure_parser(subparser)
                subparser.set_defaults(cmd=callback)

            @lru_cache()
            def _get_subparsers(self):
                return self._parser.add_subparsers(title="subcommands", metavar=None, help="")

    ```


### CliRequestRegistrationEvent()

```python
CliRequestRegistrationEvent(parser: argparse.ArgumentParser):
```


??? note "View Source"
    ```python
            def __init__(self, parser: ArgumentParser):
                self._parser = parser

    ```


### register_command()

```python
def register_command(self, name: str, command: seagulls.cli._request.ICliCommand) -> None:
```


??? note "View Source"
    ```python
            def register_command(self, name: str, command: ICliCommand) -> None:
                def callback() -> None:
                    command.execute()
                subparser = self._get_subparsers().add_parser(name=name)
                command.configure_parser(subparser)
                subparser.set_defaults(cmd=callback)

    ```


