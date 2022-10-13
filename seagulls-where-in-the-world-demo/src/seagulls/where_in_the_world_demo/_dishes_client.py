from typing import Tuple, NamedTuple, List


class Dish(NamedTuple):
    name: str
    description: List[str]
    country: str


class DishesClient:

    _dishes: Tuple[Dish, ...]

    def __init__(self, dishes: Tuple[Dish, ...]) -> None:
        self._dishes = dishes

    def is_final_level(self, level: int) -> bool:
        return level == len(self._dishes) - 1

    def get_level(self, level: int) -> Dish:
        if level >= len(self._dishes):
            raise RuntimeError(f"Dish for level not found: {level}")

        return self._dishes[level]
