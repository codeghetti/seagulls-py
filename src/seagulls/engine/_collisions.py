import logging
from typing import Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


def flag_from_string(value: str) -> int:
    if not isinstance(value, str):
        raise ValueError(f"Value must be a string of 0s and 1s: {value}")

    return int(value, 2)


@dataclass(frozen=True)
class CollidableObject:
    layer: int
    mask: int

    def filter_by_mask(
            self, targets: Tuple["CollidableObject", ...]) -> Tuple["CollidableObject", ...]:
        result = []
        for t in targets:
            if self.is_in_mask(t):
                result.append(t)

        return tuple(result)

    def is_in_mask(self, target: "CollidableObject") -> bool:
        logger.debug(f"targeting items located in mask: {self.mask:b}")
        logger.debug(f"target is located in layer: {target.layer:b}")
        logger.debug(f"& result: {self.mask & target.layer:b}")
        return self.mask & target.layer > 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(layer={self.layer:b}, mask={self.mask:b})"
