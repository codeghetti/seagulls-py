from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import Any, Dict


class BaseCliCommand(ABC):
    @abstractmethod
    def get_command_name(self) -> str:
        pass

    @abstractmethod
    def get_command_help(self) -> str:
        pass

    @abstractmethod
    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> None:
        pass


class CliCommand(BaseCliCommand, ABC):
    pass
