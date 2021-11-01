---
title: "API Docs: seagulls.foo.another"
---


# [seagulls](../../seagulls).[foo](../foo).another


??? note "View Source"
    ```python
        from . import _bar as bar

        __all__ = [
            "bar"
        ]

    ```

## Sumbodule:  bar

**taken from:** `seagulls.foo.another._bar`

Example submodule being exposed through `seagulls.foo.another`.


## bar.SomeFooBar

```python
class bar.SomeFooBar:
```

Blah Blah, SomeFooBar.

??? note "View Source"
    ```python
        class SomeFooBar:
            """Blah Blah, SomeFooBar."""

            thing: int = 5
            """The thing thing."""

            def do_it(self, arg: int) -> None:
                """
                Does the thing.

                Args:
                    arg: number of times to do the thing
                """

    ```


### \_\_init\_\_()

```python
bar.SomeFooBar():
```




### thing

```python
thing: int = 5
```

The thing thing.


### do_it()

```python
def do_it(self, arg: int) -> None:
```

Does the thing.


#### Args
 - **arg:**  number of times to do the thing



??? note "View Source"
    ```python
            def do_it(self, arg: int) -> None:
                """
                Does the thing.

                Args:
                    arg: number of times to do the thing
                """

    ```




Example submodule being exposed through `seagulls.foo.another`.

??? note "View Source"
    ```python
        """
        Example submodule being exposed through `seagulls.foo.another`.
        """


        class SomeFooBar:
            """Blah Blah, SomeFooBar."""

            thing: int = 5
            """The thing thing."""

            def do_it(self, arg: int) -> None:
                """
                Does the thing.

                Args:
                    arg: number of times to do the thing
                """

    ```


