import random
from abc import abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from typing import Protocol, Tuple, NamedTuple, List

import pygame.image

from seagulls.engine import Surface
from seagulls.where_in_the_world_demo._trivia import get_food_trivia, get_foods
from seagulls.where_in_the_world_demo._trivia_image import generate_image


class Dish(NamedTuple):
    name: str
    description: List[str]
    country: str


@dataclass(frozen=True)
class DishInput:
    country: str


class IDishesClient(Protocol):
    @abstractmethod
    def is_final_level(self, level: int) -> bool:
        pass

    @abstractmethod
    def get_dish_image(self, level: int) -> Surface:
        pass

    @abstractmethod
    def get_level(self, level: int) -> Dish:
        pass


class DishesClient(IDishesClient):

    _dishes: Tuple[Dish, ...]

    def __init__(self, dishes: Tuple[Dish, ...]) -> None:
        self._dishes = dishes

    def is_final_level(self, level: int) -> bool:
        return level == len(self._dishes) - 1

    def get_dish_image(self, level: int) -> Surface:
        pass

    def get_level(self, level: int) -> Dish:
        if level >= len(self._dishes):
            raise RuntimeError(f"Dish for level not found: {level}")

        return self._dishes[level]


class GptDishesClient(IDishesClient):

    _inputs: Tuple[DishInput, ...]

    def __init__(self, inputs: Tuple[DishInput, ...]) -> None:
        self._inputs = inputs

    def is_final_level(self, level: int) -> bool:
        return level == len(self._inputs) - 1

    @lru_cache()
    def get_dish_image(self, level: int) -> Surface:
        dish = self.get_level(level)
        filename = generate_image(food=dish.name, country=dish.country)
        return pygame.image.load(filename).convert()

    @lru_cache()
    def get_level(self, level: int) -> Dish:
        if level >= len(self._inputs):
            raise RuntimeError(f"Dish for level not found: {level}")

        level_input = self._inputs[level]
        food_name = random.choice(get_foods(level_input.country))
        clue = get_food_trivia(food_name, level_input.country)

        def listify(text: str) -> List[str]:
            lines = []
            line = ""
            for word in text.split():
                if len(line) + len(word) > 49:
                    lines.append(line)
                    line = ""
                line += word + " "
            lines.append(line)
            return lines

        return Dish(
            name=food_name,
            description=listify(clue),
            country=level_input.country,
        )
