from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Dependency

from ._example_command import ExampleCommand
from ._launch_command import LaunchCommand
from ._logging_client import LoggingClient
from ._root_command import RootCommand


class SeagullsDiContainer(DeclarativeContainer):
    _logging_verbosity = Dependency(instance_of=int)
    logging_client = Singleton(
        LoggingClient,
        verbosity=_logging_verbosity,
    )

    root_command = Singleton(RootCommand)
    launch_command = Singleton(LaunchCommand)

    example_command = Singleton(ExampleCommand)
