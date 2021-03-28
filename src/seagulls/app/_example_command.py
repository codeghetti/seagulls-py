from argparse import ArgumentParser
from typing import Any, Dict

from ._command_interfaces import CliCommand


class ExampleCommand(CliCommand):
    def get_command_name(self) -> str:
        return "example"

    def get_command_help(self) -> str:
        return "Just an example command"

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self, args: Dict[str, Any]) -> None:
        print("I don't do anything useful")
