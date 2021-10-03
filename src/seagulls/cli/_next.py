import os
import logging
from abc import ABC
from typing import Tuple, Generic, TypeVar

import pygame

from ._di_container import SeagullsDiContainer

logger = logging.getLogger(__name__)
T = TypeVar('T')


class CliCommand(Generic[T], ABC):
    def execute(self, request: T) -> None:
        pass


class FooRequest:
    pass


class FooCliCommand(CliCommand[FooRequest]):
    def execute(self, request: FooRequest) -> None:
        print("Hello, World!")


class CliCommandLocator:
    def find_command(self, args: Tuple[str, ...]) -> CliCommand:
        return FooCliCommand()


class CliClient:

    _command_locator: CliCommandLocator

    def __init__(self, command_locator: CliCommandLocator):
        self._command_locator = command_locator

    def execute(self, args: Tuple[str, ...]) -> None:
        command = self._command_locator.find_command(args)
        command.execute()


def cli_next():
    # Got tired of running into exceptions when this isn't initialized in time.
    pygame.init()

    logging_verbosity = int(os.environ.get("VERBOSITY", "3"))
    if "DEBUG" in os.environ:
        logging_verbosity = 100  # 100 is higher than any log level we will ever have

    di_container = SeagullsDiContainer(_logging_verbosity=logging_verbosity)
    logging_client = di_container.logging_client()
    logging_client.configure_logging()

    root_command = di_container.root_command()

    # # Build the CLI Command Interface
    # parser = ArgumentParser(
    #     description=root_command.get_command_help(),
    # )
    # parser.set_defaults(cmd=root_command)
    # parser.set_defaults(parser=parser)
    #
    # root_command.configure_parser(parser)
    #
    # sub_commands = parser.add_subparsers(title="subcommands", metavar=None, help="")
    #
    # for provider in di_container.traverse():
    #     provided = provider.provides
    #     try:
    #         is_command = issubclass(provided, CliCommand)
    #     except TypeError:
    #         continue
    #
    #     if not is_command:
    #         continue
    #
    #     logger.info(f"Initializing CliCommand: {provided}")
    #     cmd: CliCommand = provider()
    #     subparser = sub_commands.add_parser(
    #         name=cmd.get_command_name(),
    #         help=cmd.get_command_help(),
    #     )
    #     cmd.configure_parser(subparser)
    #     subparser.set_defaults(cmd=cmd)
    #
    # args = parser.parse_args(sys.argv[1:])
    # matched_cmd: CliCommand = args.cmd
    # matched_cmd.execute(vars(args))
