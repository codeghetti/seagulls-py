---
title: "API Docs: seagulls.foo.test_base"
---


# [seagulls](../../seagulls).[foo](../foo).test_base


??? note "View Source"
    ```python
        class SomeBaseClass:
            """
            Documentation for `SomeBaseClass`.
            """

            base_property: str
            """
            Documentation for `SomeBaseClass.base_property`.
            """

            base_property_with_default: str = "hello"
            """
            Documentation for `SomeBaseClass.base_property_with_default`.
            """

            def __init__(self, arg1: str):
                """
                This is the documentation for `SomeBaseClass.__init__()`.

                Args:
                    arg1: The docs for arg1 arg in `SomeBaseClass.__init__()`.
                """
                super().__init__()
                pass

            def some_base_method(self, arg1: int, *args, **kwargs) -> None:
                """
                This is the documentation for `SomeBaseClass.some_base_method()`.
                """
                pass


        class AnotherBaseClass(SomeBaseClass):
            """
            Documentation for `AnotherBaseClass`.
            """

            another_property: str
            """
            Documentation for `AnotherBaseClass.another_property`.
            """

            def another_base_method(self, arg1: int, *args, **kwargs) -> None:
                """
                This is the documentation for `AnotherBaseClass.another_base_method()`.
                """
                pass

    ```

## SomeBaseClass

```python
class SomeBaseClass:
```

Documentation for `SomeBaseClass`.

??? note "View Source"
    ```python
        class SomeBaseClass:
            """
            Documentation for `SomeBaseClass`.
            """

            base_property: str
            """
            Documentation for `SomeBaseClass.base_property`.
            """

            base_property_with_default: str = "hello"
            """
            Documentation for `SomeBaseClass.base_property_with_default`.
            """

            def __init__(self, arg1: str):
                """
                This is the documentation for `SomeBaseClass.__init__()`.

                Args:
                    arg1: The docs for arg1 arg in `SomeBaseClass.__init__()`.
                """
                super().__init__()
                pass

            def some_base_method(self, arg1: int, *args, **kwargs) -> None:
                """
                This is the documentation for `SomeBaseClass.some_base_method()`.
                """
                pass

    ```


### SomeBaseClass()

```python
SomeBaseClass(arg1: str):
```

This is the documentation for `SomeBaseClass.__init__()`.


#### Args
 - **arg1:**  The docs for arg1 arg in `SomeBaseClass.__init__()`.



??? note "View Source"
    ```python
            def __init__(self, arg1: str):
                """
                This is the documentation for `SomeBaseClass.__init__()`.

                Args:
                    arg1: The docs for arg1 arg in `SomeBaseClass.__init__()`.
                """
                super().__init__()
                pass

    ```


### base_property

```python
base_property: str
```

Documentation for `SomeBaseClass.base_property`.


### base_property_with_default

```python
base_property_with_default: str = 'hello'
```

Documentation for `SomeBaseClass.base_property_with_default`.


### some_base_method()

```python
def some_base_method(self, arg1: int, *args, **kwargs) -> None:
```

This is the documentation for `SomeBaseClass.some_base_method()`.

??? note "View Source"
    ```python
            def some_base_method(self, arg1: int, *args, **kwargs) -> None:
                """
                This is the documentation for `SomeBaseClass.some_base_method()`.
                """
                pass

    ```


## AnotherBaseClass

```python
class AnotherBaseClass(SomeBaseClass):
```

Documentation for `AnotherBaseClass`.

??? note "View Source"
    ```python
        class AnotherBaseClass(SomeBaseClass):
            """
            Documentation for `AnotherBaseClass`.
            """

            another_property: str
            """
            Documentation for `AnotherBaseClass.another_property`.
            """

            def another_base_method(self, arg1: int, *args, **kwargs) -> None:
                """
                This is the documentation for `AnotherBaseClass.another_base_method()`.
                """
                pass

    ```


### another_property

```python
another_property: str
```

Documentation for `AnotherBaseClass.another_property`.


### another_base_method()

```python
def another_base_method(self, arg1: int, *args, **kwargs) -> None:
```

This is the documentation for `AnotherBaseClass.another_base_method()`.

??? note "View Source"
    ```python
            def another_base_method(self, arg1: int, *args, **kwargs) -> None:
                """
                This is the documentation for `AnotherBaseClass.another_base_method()`.
                """
                pass

    ```


### Inherited Members

**taken from:** seagulls.foo.test_base:SomeBaseClass

- `#!python SomeBaseClass(arg1: str)`
- `#!python base_property: str`
- `#!python base_property_with_default: str = 'hello'`
- `#!python some_base_method(arg1: int, *args, **kwargs) -> None`
