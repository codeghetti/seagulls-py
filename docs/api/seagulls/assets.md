---
title: "API Docs: seagulls.assets"
---


# [seagulls](../seagulls).assets


??? note "View Source"
    ```python
        from ._manager import AssetManager

        __all__ = ["AssetManager"]

    ```

## AssetManager

```python
class AssetManager:
```

Provides basic functionality for loading assets from disk.

??? note "View Source"
    ```python
        class AssetManager:

            """Provides basic functionality for loading assets from disk."""

            _assets_path: Path

            def __init__(self, assets_path: Path):
                self._assets_path = assets_path

            def load_sprite(self, name: str) -> Surface:
                return self.load_png(f"sprites/{name}")

            def load_png(self, name: str) -> Surface:
                path = self._assets_path / f"{name}.png"
                loaded_sprite = load(path.resolve())
                if loaded_sprite.get_alpha() is None:
                    return loaded_sprite.convert()
                else:
                    return loaded_sprite.convert_alpha()

    ```


### \_\_init\_\_()

```python
AssetManager(assets_path: pathlib.Path):
```


??? note "View Source"
    ```python
            def __init__(self, assets_path: Path):
                self._assets_path = assets_path

    ```


### load_sprite()

```python
def load_sprite(self, name: str) -> pygame.Surface:
```


??? note "View Source"
    ```python
            def load_sprite(self, name: str) -> Surface:
                return self.load_png(f"sprites/{name}")

    ```


### load_png()

```python
def load_png(self, name: str) -> pygame.Surface:
```


??? note "View Source"
    ```python
            def load_png(self, name: str) -> Surface:
                path = self._assets_path / f"{name}.png"
                loaded_sprite = load(path.resolve())
                if loaded_sprite.get_alpha() is None:
                    return loaded_sprite.convert()
                else:
                    return loaded_sprite.convert_alpha()

    ```


