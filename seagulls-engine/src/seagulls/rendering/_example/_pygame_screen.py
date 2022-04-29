from seagulls.rendering._example._scene import SceneProvider


class PygameScreen:
    _scene: SceneProvider

    def __init__(self, scene: SceneProvider):
        self._scene = scene

    def refresh(self) -> None:
        self._scene.get().tick()
