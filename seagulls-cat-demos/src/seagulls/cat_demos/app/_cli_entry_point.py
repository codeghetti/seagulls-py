from seagulls.app import ISeagullsApplicationPluginRegistrant
from seagulls.seagulls_cli import (
    SeagullsAppDiContainer,
    SeagullsCliApplication
)

from seagulls.cat_demos.app._di_container import CatDemosDiContainer


class CatDemosCliPluginEntryPoint(
        ISeagullsApplicationPluginRegistrant[SeagullsCliApplication]):

    @staticmethod
    def register_plugins(application: SeagullsCliApplication) -> None:
        di_container = CatDemosDiContainer(application=application)
        application.register_plugin(di_container.plugin())


def _main():
    di_container = SeagullsAppDiContainer(tuple(["seagulls", "launch"]))
    app = di_container.application()
    rpg_demo_di_container = CatDemosDiContainer(application=app)
    app.register_plugin(rpg_demo_di_container.plugin())
    app.execute()


if __name__ == '__main__':
    _main()
