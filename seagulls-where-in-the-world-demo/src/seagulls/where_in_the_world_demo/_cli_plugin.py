from seagulls.app import ISeagullsApplicationPlugin
from seagulls.cli import CliRequestRegistrationEvent, ICliCommand
from seagulls.seagulls_cli import SeagullsCliApplication


class WhereInTheWorldDemoCliPlugin(ISeagullsApplicationPlugin):

    _application: SeagullsCliApplication
    _command: ICliCommand

    def __init__(self, application: SeagullsCliApplication, command: ICliCommand):
        self._application = application
        self._command = command

    def on_registration(self) -> None:
        self._application.register_callback(
            CliRequestRegistrationEvent, self._on_cli_request_registration)

    def _on_cli_request_registration(self, event: CliRequestRegistrationEvent) -> None:
        event.register_command("launch", self._command)
