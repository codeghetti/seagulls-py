from pathlib import Path

import pytest

from seagulls.assets import AssetManager


class TestAssetManager:
    def test_nothing(self) -> None:
        assert AssetManager

    def test_get_path(self) -> None:
        client = AssetManager(Path("."))
        expected = Path("pyproject.toml")
        assert client.get_path("pyproject.toml") == expected

        with pytest.raises(RuntimeError):
            client.get_path("missing-file.txt")
