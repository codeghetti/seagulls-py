import math
from typing import Tuple, NamedTuple

from ._position import Position


class Country(NamedTuple):
    name: str
    position: Position

    def distance(self, position: Position) -> int:
        return abs(int(math.hypot(self.position.x - position.x, self.position.y - position.y)))


class CountriesClient:

    _countries: Tuple[Country, ...]

    def __init__(self, countries: Tuple[Country, ...]) -> None:
        self._countries = countries

    def get_countries(self) -> Tuple[Country, ...]:
        return self._countries

    def get_country(self, name: str) -> Country:
        for country in self._countries:
            if country.name == name:
                return country

        raise RuntimeError(f"Country not found: {name}")
