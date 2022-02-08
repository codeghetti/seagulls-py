from seagulls.app import ISeagullsApplicationPlugin
from seagulls.cli import CliRequestRegistrationEvent

from seagulls.seagulls_cli import SeagullsCliApplication
from ._flake8_command import Flake8Command
from ._mypy_command import MypyCommand
from ._publish_command import PublishWheelCommand
from ._pytest_command import PytestCommand


class DevtoolsCliPlugin(ISeagullsApplicationPlugin):

    _application: SeagullsCliApplication
    _flake8_command: Flake8Command
    _mypy_command: MypyCommand
    _pytest_command: PytestCommand
    _publish_command: PublishWheelCommand

    def __init__(
            self,
            application: SeagullsCliApplication,
            flake8_command: Flake8Command,
            mypy_command: MypyCommand,
            pytest_command: PytestCommand,
            publish_command: PublishWheelCommand):
        self._application = application
        self._flake8_command = flake8_command
        self._mypy_command = mypy_command
        self._pytest_command = pytest_command
        self._publish_command = publish_command

    def on_registration(self) -> None:
        self._application.register_callback(
            CliRequestRegistrationEvent, self._on_cli_request_registration)

    def _on_cli_request_registration(
            self, event: CliRequestRegistrationEvent) -> None:
        event.register_command("flake8", self._flake8_command)
        event.register_command("mypy", self._mypy_command)
        event.register_command("pytest", self._pytest_command)
        event.register_command("publish", self._publish_command)
