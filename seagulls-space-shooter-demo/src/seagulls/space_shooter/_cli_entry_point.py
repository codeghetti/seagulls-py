from seagulls.app import ISeagullsApplicationPluginRegistrant
from seagulls.cli_next import SeagullsCliApplication
from ._di_container import SpaceShooterDiContainer


class SpaceShooterCliPluginEntryPoint(
        ISeagullsApplicationPluginRegistrant[SeagullsCliApplication]):

    @staticmethod
    def register_plugins(application: SeagullsCliApplication) -> None:
        di_container = SpaceShooterDiContainer(application=application)
        application.register_plugin(di_container.plugin())
