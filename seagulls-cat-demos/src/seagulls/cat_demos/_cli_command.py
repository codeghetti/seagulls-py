from argparse import ArgumentParser
from seagulls.cli import ICliCommand


class GameCliCommand(ICliCommand):

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        print("coming soon!")
