import logging
import subprocess
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

import toml
from seagulls.cli import ICliCommand

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProgramDetails:
    name: str
    entry_point_path: Path
    project_path: Path


class BuildExecutableCommand(ICliCommand):

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        details = self._load_program_details()

        cmd = [
            "pyinstaller",
            str(details.entry_point_path),
            "--add-data", f"{details.project_path.resolve()}/seagulls_assets:seagulls_assets",
            "--distpath", f"../.tmp/{details.name}/dist/",
            "--workpath", f"../.tmp/{details.name}/build/",
            "--specpath", f"../.tmp/{details.name}/",
            "--name", details.name,
            "--clean",
        ]

        subprocess.run(cmd, check=True)

    def _load_program_details(self) -> ProgramDetails:
        pyproject_path = Path("pyproject.toml")
        project_path = pyproject_path.parent

        if not pyproject_path.is_file():
            raise RuntimeError("Required pyproject.toml file not found")

        pyproject = toml.load(str(pyproject_path))
        seagulls = pyproject.get("tool", {}).get("seagulls", {})

        return ProgramDetails(
            name=seagulls.get("name"),
            entry_point_path=Path(seagulls.get("entry_point_path")),
            project_path=project_path,
        )
