from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import yaml


class GameSettings:

    def get_setting(self, name, default=None) -> Any:
        data = self._load_yaml()
        return data.get(name, default)

    @lru_cache()
    def _load_yaml(self) -> Dict[str, Any]:
        file = Path.home() / ".config/seagulls.yaml"
        if not file.exists():
            file.touch()

        return yaml.safe_load(file.read_text()) or {}
