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


        class SomeClass(str):
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
class SomeClass(builtins.str):
```

Documentation for `SomeClass`.

??? note "View Source"
    ```python
        class SomeClass(str):
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


### \_\_init\_\_()

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
(&#39;builtins&#39;, &#39;str&#39;)
- [encode]((&#39;builtins&#39;, &#39;str.encode&#39;))
- [replace]((&#39;builtins&#39;, &#39;str.replace&#39;))
- [split]((&#39;builtins&#39;, &#39;str.split&#39;))
- [rsplit]((&#39;builtins&#39;, &#39;str.rsplit&#39;))
- [join]((&#39;builtins&#39;, &#39;str.join&#39;))
- [capitalize]((&#39;builtins&#39;, &#39;str.capitalize&#39;))
- [casefold]((&#39;builtins&#39;, &#39;str.casefold&#39;))
- [title]((&#39;builtins&#39;, &#39;str.title&#39;))
- [center]((&#39;builtins&#39;, &#39;str.center&#39;))
- [count]((&#39;builtins&#39;, &#39;str.count&#39;))
- [expandtabs]((&#39;builtins&#39;, &#39;str.expandtabs&#39;))
- [find]((&#39;builtins&#39;, &#39;str.find&#39;))
- [partition]((&#39;builtins&#39;, &#39;str.partition&#39;))
- [index]((&#39;builtins&#39;, &#39;str.index&#39;))
- [ljust]((&#39;builtins&#39;, &#39;str.ljust&#39;))
- [lower]((&#39;builtins&#39;, &#39;str.lower&#39;))
- [lstrip]((&#39;builtins&#39;, &#39;str.lstrip&#39;))
- [rfind]((&#39;builtins&#39;, &#39;str.rfind&#39;))
- [rindex]((&#39;builtins&#39;, &#39;str.rindex&#39;))
- [rjust]((&#39;builtins&#39;, &#39;str.rjust&#39;))
- [rstrip]((&#39;builtins&#39;, &#39;str.rstrip&#39;))
- [rpartition]((&#39;builtins&#39;, &#39;str.rpartition&#39;))
- [splitlines]((&#39;builtins&#39;, &#39;str.splitlines&#39;))
- [strip]((&#39;builtins&#39;, &#39;str.strip&#39;))
- [swapcase]((&#39;builtins&#39;, &#39;str.swapcase&#39;))
- [translate]((&#39;builtins&#39;, &#39;str.translate&#39;))
- [upper]((&#39;builtins&#39;, &#39;str.upper&#39;))
- [startswith]((&#39;builtins&#39;, &#39;str.startswith&#39;))
- [endswith]((&#39;builtins&#39;, &#39;str.endswith&#39;))
- [removeprefix]((&#39;builtins&#39;, &#39;str.removeprefix&#39;))
- [removesuffix]((&#39;builtins&#39;, &#39;str.removesuffix&#39;))
- [isascii]((&#39;builtins&#39;, &#39;str.isascii&#39;))
- [islower]((&#39;builtins&#39;, &#39;str.islower&#39;))
- [isupper]((&#39;builtins&#39;, &#39;str.isupper&#39;))
- [istitle]((&#39;builtins&#39;, &#39;str.istitle&#39;))
- [isspace]((&#39;builtins&#39;, &#39;str.isspace&#39;))
- [isdecimal]((&#39;builtins&#39;, &#39;str.isdecimal&#39;))
- [isdigit]((&#39;builtins&#39;, &#39;str.isdigit&#39;))
- [isnumeric]((&#39;builtins&#39;, &#39;str.isnumeric&#39;))
- [isalpha]((&#39;builtins&#39;, &#39;str.isalpha&#39;))
- [isalnum]((&#39;builtins&#39;, &#39;str.isalnum&#39;))
- [isidentifier]((&#39;builtins&#39;, &#39;str.isidentifier&#39;))
- [isprintable]((&#39;builtins&#39;, &#39;str.isprintable&#39;))
- [zfill]((&#39;builtins&#39;, &#39;str.zfill&#39;))
- [format]((&#39;builtins&#39;, &#39;str.format&#39;))
- [format_map]((&#39;builtins&#39;, &#39;str.format_map&#39;))
- [maketrans]((&#39;builtins&#39;, &#39;str.maketrans&#39;))
