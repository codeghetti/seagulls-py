import logging
import os
import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generic, List, Tuple, TypeVar

import pygame

from seagulls.cli._di_container import SeagullsDiContainer

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


class IExecuteCommands(ABC):

    @abstractmethod
    def execute(self, args: Tuple[str, ...]) -> None:
        pass


class IRegisterCliCommands(ABC):

    @abstractmethod
    def register_command(self, path: Tuple[str, ...], command: IExecuteCommands) -> None:
        pass


@dataclass(frozen=True)
class CommandRequestItem:
    path: Tuple[str, ...]
    command: IExecuteCommands

    def trim_prefix(self, args: Tuple[str, ...]) -> Tuple[str, ...]:
        current = list(args)
        for y in self.path:
            current = current[current.index(y):]

        return tuple(current)

    def trim_suffix(self, args: Tuple[str, ...], next_path: Tuple[str, ...]) -> Tuple[str, ...]:
        parts = next_path
        parts = parts[len(parts) - 1:]
        next_current = list(args)
        print(f"not last: {self}")
        print(f"adjusting current with additional: {parts}")
        for y in parts:
            next_current = next_current[next_current.index(y):]
            print(f"additional y: {y}")
            print(f"current: {args}")
        print(f"NEXT CURRENT: {next_current}")
        adjusted_current = args[:-1 * len(next_current)]
        print(f"adjusted current: {adjusted_current}")
        return adjusted_current


@dataclass(frozen=True)
class CommandRequest:
    chain: Tuple[CommandRequestItem, ...]


class CliCommandArgs:
    _args: Tuple[str, ...]

    def __init__(self, args: Tuple[str, ...]):
        self._args = args


class IBuildCommandRequests(ABC):

    @abstractmethod
    def build_command_request(self, args: Tuple[str, ...]) -> CommandRequest:
        pass


class CliCommandsRegistry(IRegisterCliCommands):
    _entries: Dict[Tuple[str, ...], IExecuteCommands]

    def __init__(self):
        self._entries = {}

    def get_dict(self) -> Dict[Tuple[str, ...], IExecuteCommands]:
        return self._entries

    def register_command(self, path: Tuple[str, ...], command: IExecuteCommands) -> None:
        self._validate_path(path)

        if path in self._entries:
            raise RuntimeError(f"Path already reserved: {path}")

        self._entries[path] = command

    def _validate_path(self, path: Tuple[str, ...]) -> None:
        for item in path:
            # all lowercase letters, numbers, and dashes but cannot start or end with a dash
            if not re.match("^[a-z0-9][a-z0-9-]+[a-z0-9]$", item):
                raise RuntimeError(f"Invalid CLI Command Part: {item}")

            if "--" in item:
                # no consecutive dashes allowed, either
                raise RuntimeError(f"Invalid CLI Command Part: {item}")


class ExampleCommand(IExecuteCommands):

    _with_route: Tuple[str, ...]

    def __init__(self, with_route: Tuple[str, ...]):
        self._with_route = with_route

    def execute(self, args: Tuple[str, ...]) -> None:
        print(f"EXECUTED: {args}")
        print(f"WITH ROUTE: {self._with_route}")


class CliClient(IBuildCommandRequests):

    _registry: CliCommandsRegistry

    def __init__(self, registry: CliCommandsRegistry):
        self._registry = registry

    def execute(self, args: Tuple[str, ...]) -> None:
        request = self.build_command_request(args)
        print(f"request: {request}")
        print("")
        for x in range(len(request.chain)):
            item: CommandRequestItem = request.chain[x]
            current = list(item.trim_prefix(args))
            print(f"finding current for item: {item}")

            # on the last command, this is the args used
            print(f"current: {current}")

            if x == len(request.chain) - 1:
                print(f"last: {item}")
                item.command.execute(tuple(current))
            else:
                # but otherwise, args stops at the beginning of the args for the next command
                next_item: CommandRequestItem = request.chain[x+1]
                adjusted_current = item.trim_suffix(tuple(current), next_item.path)
                item.command.execute(tuple(adjusted_current))

            print("")

        # command = self._command_locator.find_command(args)
        # command.execute()

    def build_command_request(self, args: Tuple[str, ...]) -> CommandRequest:
        result: List[CommandRequestItem] = []
        matching_path = []
        for arg in args:
            if not re.match("^[a-z0-9][a-z0-9-]+[a-z0-9]$", arg):
                continue

            matching_path.append(arg)

        mapping = self._registry.get_dict()
        print(f"mapping: {mapping}")

        for x in range(len(matching_path) + 1):
            index = x - len(matching_path)
            subset = tuple(matching_path[:index] if index else matching_path)
            print(f"testing: {subset}")
            if subset in mapping:
                print(f"match: {subset}: {mapping[subset]}")
                result.append(CommandRequestItem(path=subset, command=mapping[subset]))

        return CommandRequest(chain=tuple(result))


if __name__ == "__main__":
    registry_client = CliCommandsRegistry()
    registry_client.register_command(
        ("example",), ExampleCommand(("example",)))

    registry_client.register_command(
        ("example", "one"), ExampleCommand(("example", "one")))

    registry_client.register_command(
        ("example", "one", "two", "bar"), ExampleCommand(("example", "one", "two", "bar")))

    registry_client.register_command(
        ("example", "foobar"), ExampleCommand(("example", "foobar")))

    client = CliClient(registry_client)
    client.execute(tuple(sys.argv[1:]))


def cli_next():
    # Got tired of running into exceptions when this isn't initialized in time.
    pygame.init()

    logging_verbosity = int(os.environ.get("VERBOSITY", "3"))
    if "DEBUG" in os.environ:
        logging_verbosity = 100  # 100 is higher than any log level we will ever have

    di_container = SeagullsDiContainer(_logging_verbosity=logging_verbosity)
    logging_client = di_container.logging_client()
    logging_client.configure_logging()

    # root_command = di_container.root_command()

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
