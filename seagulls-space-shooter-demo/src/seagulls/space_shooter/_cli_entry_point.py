from seagulls.app import ISeagullsApplicationPluginRegistrant
from seagulls.seagulls_cli import (
    SeagullsAppDiContainer,
    SeagullsCliApplication
)

from seagulls.space_shooter._di_container import SpaceShooterDiContainer


class SpaceShooterCliPluginEntryPoint(
        ISeagullsApplicationPluginRegistrant[SeagullsCliApplication]):

    @staticmethod
    def register_plugins(application: SeagullsCliApplication) -> None:
        di_container = SpaceShooterDiContainer(application=application)
        application.register_plugin(di_container.plugin())


def _main():
    di_container = SeagullsAppDiContainer(tuple(["seagulls", "launch"]))
    app = di_container.application()
    space_shooter_di_container = SpaceShooterDiContainer(application=app)
    app.register_plugin(space_shooter_di_container.plugin())
    app.execute()


if __name__ == '__main__':
    _main()
