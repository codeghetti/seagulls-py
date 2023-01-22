from pathlib import Path


class ResourceClient:

    def get_path(self, resource: str) -> Path:
        # TODO: need a real implementation here.
        p = Path("resources") / resource.lstrip("/")
        if not p.exists():
            raise RuntimeError(f"Resource not found: {resource}")

        return p
