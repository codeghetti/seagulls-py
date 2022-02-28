from abc import abstractmethod
from argparse import ArgumentParser
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional, Protocol, Tuple

from seagulls.eventing import IDispatchEvents

EnvironmentTuple = Tuple[str, str]


class RequestEnvironment:

    _values: Dict[str, str]

    def __init__(self, values: Tuple[EnvironmentTuple, ...]):
        self._values = {k: v for k, v in values}

    def get(self, name: str, default: str = None) -> Optional[str]:
        return self._values.get(name, default)

    def as_dict(self) -> Dict[str, str]:
        return self._values.copy()


class ICliCommand(Protocol):

    @abstractmethod
    def configure_parser(self, parser: ArgumentParser) -> None:
        """
        Do your thing.
        """

    @abstractmethod
    def execute(self) -> None:
        """
        Do your thing.
        """


class CliRequestRegistrationEvent:

    _parser: ArgumentParser

    def __init__(self, parser: ArgumentParser):
        self._parser = parser

    def register_command(self, name: str, command: ICliCommand) -> None:
        def callback() -> None:
            command.execute()
        subparser = self._get_subparsers().add_parser(name=name)
        command.configure_parser(subparser)
        subparser.set_defaults(cmd=callback)

    @lru_cache()
    def _get_subparsers(self):
        return self._parser.add_subparsers(title="subcommands", metavar=None, help="")


class CliRequest:

    _file: Path
    _args: Tuple[str, ...]
    _env: RequestEnvironment

    def __init__(
            self,
            file: Path,
            args: Tuple[str, ...],
            env: RequestEnvironment):
        self._file = file
        self._args = args
        self._env = env

    def execute(self, event_dispatcher: IDispatchEvents) -> None:
        # Build the CLI Command Interface
        parser = ArgumentParser(
            description="Seagulls CLI Command",
        )

        event = CliRequestRegistrationEvent(parser)
        event_dispatcher.trigger_event(event)

        def default_execute() -> None:
            parser.print_help()

        parser.set_defaults(cmd=default_execute)

        args = parser.parse_args(self._args)
        args.cmd()
