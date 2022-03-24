from seagulls.seagulls_cli import SeagullsCliApplication

from ._cli_plugin import DevtoolsCliPlugin
from ._flake8_command import Flake8Command
from ._mypy_command import MypyCommand
from ._publish_command import PublishWheelCommand
from ._pytest_command import PytestCommand
from ._release_command import BuildExecutableCommand


class SeagullsDevtoolsDiContainer:
    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication):
        self._application = application

    def plugin(self) -> DevtoolsCliPlugin:
        return DevtoolsCliPlugin(
            application=self._application,
            flake8_command=self._flake8_command(),
            mypy_command=self._mypy_command(),
            pytest_command=self._pytest_command(),
            publish_command=self._publish_command(),
            build_executable_command=self._build_executable_command())

    def _flake8_command(self) -> Flake8Command:
        return Flake8Command()

    def _mypy_command(self) -> MypyCommand:
        return MypyCommand()

    def _pytest_command(self) -> PytestCommand:
        return PytestCommand()

    def _publish_command(self) -> PublishWheelCommand:
        return PublishWheelCommand()

    def _build_executable_command(self) -> BuildExecutableCommand:
        return BuildExecutableCommand()
