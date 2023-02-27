from seagulls.cat_demos.engine.v2.position._position_component import Vector


class MovementClient:

    _frame_vector: Vector

    def __init__(self) -> None:
        self._frame_vector = Vector.zero()

    def reset(self) -> None:
        self._frame_vector = Vector.zero()

    def move(self, vector: Vector) -> None:
        self._frame_vector += vector

    def get_vector(self) -> Vector:
        return self._frame_vector
