import logging
import platform
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

        assets_path = details.project_path / "seagulls_assets"
        dist_path = Path(f"../.tmp/{details.name}/dist/")
        work_path = Path(f"../.tmp/{details.name}/build/")
        spec_path = Path(f"../.tmp/{details.name}/")

        system = platform.system()

        if system.lower() == "windows":
            add_data = f"{assets_path.resolve()};seagulls_assets"
        else:
            add_data = f"{assets_path.resolve()}:seagulls_assets"

        cmd = [
            "pyinstaller",
            str(details.entry_point_path),
            "--add-data", add_data,
            "--distpath", str(dist_path.resolve()),
            "--workpath", str(work_path),
            "--specpath", str(spec_path),
            "--name", details.name,
            "--onefile",
            "--noconsole",
            "--clean",
        ]

        splash_path = assets_path / "splash.png"
        ico_path = assets_path / "application.ico"

        if splash_path.is_file():
            cmd.extend(["--splash", str(splash_path.resolve())])

        if ico_path.is_file():
            cmd.extend(["--icon", str(ico_path.resolve())])

        print(f"Running: {' '.join(cmd)}")

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
