---
title: "seagulls.eventing"
---


# [seagulls](../seagulls).eventing


??? note "View Source"
    ```python
        from ._interfaces import (
            IDispatchEvents,
            EventType,
            EventCallbackType,
        )

        __all__ = [
            "IDispatchEvents",
            "EventType",
            "EventCallbackType",
        ]

    ```

## IDispatchEvents

```python
class IDispatchEvents(typing.Protocol):
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
        class IDispatchEvents(Protocol):

            @abstractmethod
            def register_callback(
                    self,
                    event_type: Type[EventType],
                    callback: EventCallbackType) -> None: ...

            def trigger_event(self, event: EventType) -> None: ...

    ```


### register_callback()

```python
@abstractmethod
def register_callback(
    self,
    event_type: Type[~EventType],
    callback: Callable[[~EventType], NoneType]
) -> None:
```


??? note "View Source"
    ```python
            @abstractmethod
            def register_callback(
                    self,
                    event_type: Type[EventType],
                    callback: EventCallbackType) -> None: ...

    ```


### trigger_event()

```python
def trigger_event(self, event: ~EventType) -> None:
```


??? note "View Source"
    ```python
            def trigger_event(self, event: EventType) -> None: ...

    ```


## EventType

```python
EventType = ~EventType
```



## EventCallbackType

```python
EventCallbackType = typing.Callable[[~EventType], NoneType]
```



