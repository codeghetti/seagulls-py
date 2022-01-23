import subprocess
import sys
from argparse import ArgumentParser

from seagulls.cli import ICliCommand


class MypyCommand(ICliCommand):

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        cmd = [
            "poetry", "run",
            "mypy",
            "-p", "seagulls",
            "-p", "seagulls_test",
        ]
        try:
            subprocess.run(cmd, check=True)
            print("All Checks Passed :)")
        except subprocess.CalledProcessError:
            print("Errors Detected")
            sys.exit(1)
