import logging
import shutil
import subprocess
from argparse import ArgumentParser
from pathlib import Path

from seagulls.cli import ICliCommand

logger = logging.getLogger(__name__)


class PublishWheelCommand(ICliCommand):

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        dist_dir = Path("dist")

        if dist_dir.is_file():
            raise RuntimeError("invalid dist directory detected")

        shutil.rmtree(dist_dir)

        subprocess.run(["poetry", "build", "--format", "wheel"], check=True)
        subprocess.run(["poetry", "publish", "--no-interaction"], check=True)
