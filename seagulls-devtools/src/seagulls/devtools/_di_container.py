from seagulls.seagulls_cli import SeagullsCliApplication

from ._cli_plugin import DevtoolsCliPlugin
from ._flake8_command import Flake8Command
from ._mypy_command import MypyCommand
from ._pytest_command import PytestCommand


class SeagullsDevtoolsDiContainer:
    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication):
        self._application = application

    def plugin(self) -> DevtoolsCliPlugin:
        return DevtoolsCliPlugin(
            application=self._application,
            flake8_command=self._flake8_command(),
            mypy_command=self._mypy_command(),
            pytest_command=self._pytest_command())

    def _flake8_command(self) -> Flake8Command:
        return Flake8Command()

    def _mypy_command(self) -> MypyCommand:
        return MypyCommand()

    def _pytest_command(self) -> PytestCommand:
        return PytestCommand()
