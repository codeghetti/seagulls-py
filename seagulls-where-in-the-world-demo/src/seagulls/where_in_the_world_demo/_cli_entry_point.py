from seagulls.app import ISeagullsApplicationPluginRegistrant
from seagulls.seagulls_cli import (
    SeagullsAppDiContainer,
    SeagullsCliApplication
)

from seagulls.where_in_the_world_demo._di_container import WhereInTheWorldDemoDiContainer


class WhereInTheWorldDemoCliPluginEntryPoint(
        ISeagullsApplicationPluginRegistrant[SeagullsCliApplication]):

    @staticmethod
    def register_plugins(application: SeagullsCliApplication) -> None:
        di_container = WhereInTheWorldDemoDiContainer(application=application)
        application.register_plugin(di_container.plugin())


def _main():
    di_container = SeagullsAppDiContainer(tuple(["seagulls", "launch"]))
    app = di_container.application()
    # demo_di_container = WhereInTheWorldDemoDiContainer(application=app)
    # app.register_plugin(demo_di_container.plugin())
    app.execute()


if __name__ == '__main__':
    _main()
