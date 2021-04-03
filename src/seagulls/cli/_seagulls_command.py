from argparse import ArgumentParser
from typing import Dict, Any

from ._framework import RootCliCommand


class SeagullsCommand(RootCliCommand):

    def get_command_name(self) -> str:
        return "seagulls"

    def get_command_help(self) -> str:
        return "Seagulls are dangerous."

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("--something", help="Does nothing useful")

    def execute(self, args: Dict[str, Any]) -> None:
        args["parser"].print_help()
