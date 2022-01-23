import subprocess
import sys
from argparse import ArgumentParser

from seagulls.cli import ICliCommand


class PytestCommand(ICliCommand):

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        cmd = ["poetry", "run", "pytest", "-s"]
        try:
            subprocess.run(cmd, check=True)
            print("All Checks Passed :)")
        except subprocess.CalledProcessError:
            print("Errors Detected")
            sys.exit(1)
