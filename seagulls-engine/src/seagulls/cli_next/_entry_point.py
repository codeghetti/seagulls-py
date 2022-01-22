from ._di_container import SeagullsAppDiContainer


def main():
    di_container = SeagullsAppDiContainer()
    app = di_container.application()
    app.execute()
