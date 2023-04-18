from seagulls.app import ISeagullsApplicationPlugin
from seagulls.cli import CliRequestRegistrationEvent, ICliCommand
from seagulls.seagulls_cli import SeagullsCliApplication


class CatDemosCliPlugin(ISeagullsApplicationPlugin):

    _application: SeagullsCliApplication
    _launch_command: ICliCommand
    _dev_command: ICliCommand

    def __init__(self, application: SeagullsCliApplication, launch_command: ICliCommand, dev_command: ICliCommand):
        self._application = application
        self._launch_command = launch_command
        self._dev_command = dev_command

    def on_registration(self) -> None:
        self._application.register_callback(
            CliRequestRegistrationEvent, self._on_cli_request_registration)

    def _on_cli_request_registration(self, event: CliRequestRegistrationEvent) -> None:
        event.register_command("launch", self._launch_command)
        event.register_command("dev", self._dev_command)
