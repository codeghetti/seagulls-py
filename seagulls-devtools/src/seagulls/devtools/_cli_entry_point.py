from seagulls.app import ISeagullsApplicationPluginRegistrant
from seagulls.seagulls_cli import SeagullsCliApplication

from ._di_container import SeagullsDevtoolsDiContainer


class DevtoolsCliPluginEntryPoint(
        ISeagullsApplicationPluginRegistrant[SeagullsCliApplication]):

    @staticmethod
    def register_plugins(application: SeagullsCliApplication) -> None:
        di_container = SeagullsDevtoolsDiContainer(application=application)
        application.register_plugin(di_container.plugin())
