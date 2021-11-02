---
title: "API Docs: seagulls.foo.test"
---


# [seagulls](../../seagulls).[foo](../foo).test

This is the comment for the module.

??? note "View Source"
    ```python
        """
        This is the comment for the module.
        """
        from functools import lru_cache
        from typing import Optional

        from seagulls.foo.test_base import AnotherBaseClass

        some_variable = 10
        """
        Just commenting about `some_variable`.
        """


        def some_function(arg1: str, arg2: int) -> Optional[str]:
            """
            This is the documentation for `some_function`.

            Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.
            Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.
            Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.

            Args:
                arg1: docs for `some_function()` arg arg1.
                arg2: docs for `some_function()` arg arg2.

            Returns:
                docs for `some_function()` return value
            """
            return "my value"


        class SomeClass(AnotherBaseClass):
            """
            Documentation for `SomeClass`.
            """

            some_property: str
            """
            Documentation for `SomeClass.some_property`.
            """

            def __init__(self, arg1: str):
                """
                This is the documentation for `SomeClass.__init__()`.

                Args:
                    arg1: The docs for arg1 arg in `SomeClass.__init__()`.
                """
                super().__init__()
                pass

            @lru_cache()
            def some_method(self) -> None:
                """
                This is the documentation for `SomeClass.some_method()`.
                """
                pass

            def undocumented_method(self, foo: int, bar: int) -> int:
                return 5

    ```

## some_variable

```python
some_variable = 10
```

Just commenting about `some_variable`.


## some_function()

```python
def some_function(arg1: str, arg2: int) -> Optional[str]:
```

This is the documentation for `some_function`.

Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.
Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.
Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.


### Args
 - **arg1:**  docs for `some_function()` arg arg1.
 - **arg2:**  docs for `some_function()` arg arg2.



### Returns
&gt; docs for `some_function()` return value


??? note "View Source"
    ```python
        def some_function(arg1: str, arg2: int) -> Optional[str]:
            """
            This is the documentation for `some_function`.

            Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.
            Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.
            Some more text. Some more text. Some more text. Some more text. Some more text. Some more text.

            Args:
                arg1: docs for `some_function()` arg arg1.
                arg2: docs for `some_function()` arg arg2.

            Returns:
                docs for `some_function()` return value
            """
            return "my value"

    ```


## SomeClass

```python
class SomeClass(seagulls.foo.test_base.AnotherBaseClass):
```

Documentation for `SomeClass`.

??? note "View Source"
    ```python
        class SomeClass(AnotherBaseClass):
            """
            Documentation for `SomeClass`.
            """

            some_property: str
            """
            Documentation for `SomeClass.some_property`.
            """

            def __init__(self, arg1: str):
                """
                This is the documentation for `SomeClass.__init__()`.

                Args:
                    arg1: The docs for arg1 arg in `SomeClass.__init__()`.
                """
                super().__init__()
                pass

            @lru_cache()
            def some_method(self) -> None:
                """
                This is the documentation for `SomeClass.some_method()`.
                """
                pass

            def undocumented_method(self, foo: int, bar: int) -> int:
                return 5

    ```


### SomeClass()

```python
SomeClass(arg1: str):
```

This is the documentation for `SomeClass.__init__()`.


#### Args
 - **arg1:**  The docs for arg1 arg in `SomeClass.__init__()`.



??? note "View Source"
    ```python
            def __init__(self, arg1: str):
                """
                This is the documentation for `SomeClass.__init__()`.

                Args:
                    arg1: The docs for arg1 arg in `SomeClass.__init__()`.
                """
                super().__init__()
                pass

    ```


### some_property

```python
some_property: str
```

Documentation for `SomeClass.some_property`.


### some_method()

```python
@lru_cache()
def some_method(self) -> None:
```

This is the documentation for `SomeClass.some_method()`.

??? note "View Source"
    ```python
            @lru_cache()
            def some_method(self) -> None:
                """
                This is the documentation for `SomeClass.some_method()`.
                """
                pass

    ```


### undocumented_method()

```python
def undocumented_method(self, foo: int, bar: int) -> int:
```


??? note "View Source"
    ```python
            def undocumented_method(self, foo: int, bar: int) -> int:
                return 5

    ```


### Inherited Members

**taken from:** seagulls.foo.test_base:AnotherBaseClass

- `#!python another_property: str`
- `#!python another_base_method(arg1: int, *args, **kwargs) -> None`

**taken from:** seagulls.foo.test_base:SomeBaseClass

- `#!python base_property: str`
- `#!python base_property_with_default: str = 'hello'`
- `#!python some_base_method(arg1: int, *args, **kwargs) -> None`
