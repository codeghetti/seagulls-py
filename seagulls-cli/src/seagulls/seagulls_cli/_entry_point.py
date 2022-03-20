import sys

from ._di_container import SeagullsAppDiContainer


def main():
    di_container = SeagullsAppDiContainer(tuple(sys.argv))
    app = di_container.application()
    app.execute()
