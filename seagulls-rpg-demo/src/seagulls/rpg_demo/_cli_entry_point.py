from seagulls.app import ISeagullsApplicationPluginRegistrant
from seagulls.seagulls_cli import SeagullsCliApplication

from ._di_container import RpgDemoDiContainer


class RpgDemoCliPluginEntryPoint(
        ISeagullsApplicationPluginRegistrant[SeagullsCliApplication]):

    @staticmethod
    def register_plugins(application: SeagullsCliApplication) -> None:
        pass
        di_container = RpgDemoDiContainer(application=application)
        application.register_plugin(di_container.plugin())
