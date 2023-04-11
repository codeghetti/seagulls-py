from pathlib import Path


class ResourceClient:

    def get_path(self, name: str) -> Path:
        # TODO: fix for built games
        p = Path(f"resources/{name}")
        if not p.exists():
            raise FileNotFoundError(p)
        return p
