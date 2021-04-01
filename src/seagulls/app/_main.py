import os
import logging
import sys
from argparse import ArgumentParser

from ._command_interfaces import CliCommand
from ._di_container import SeagullsDiContainer

logger = logging.getLogger(__name__)


def main():
    logging_verbosity = int(os.environ.get("VERBOSITY", "3"))
    if "DEBUG" in os.environ:
        logging_verbosity = 100  # 100 is higher than any log level we will ever have

    di_container = SeagullsDiContainer(_logging_verbosity=logging_verbosity)
    logging_client = di_container.logging_client()
    logging_client.configure_logging()

    root_command = di_container.root_command()

    # Build the CLI Command Interface
    parser = ArgumentParser(
        description=root_command.get_command_help(),
    )
    parser.set_defaults(cmd=root_command)
    parser.set_defaults(parser=parser)

    root_command.configure_parser(parser)

    sub_commands = parser.add_subparsers(title="subcommands", metavar=None, help="")

    for provider in di_container.traverse():
        provided = provider.provides
        try:
            is_command = issubclass(provided, CliCommand)
        except TypeError:
            continue

        if not is_command:
            continue

        logger.info(f"Initializing CliCommand: {provided}")
        cmd: CliCommand = provider()
        subparser = sub_commands.add_parser(
            name=cmd.get_command_name(),
            help=cmd.get_command_help(),
        )
        cmd.configure_parser(subparser)
        subparser.set_defaults(cmd=cmd)

    args = parser.parse_args(sys.argv[1:])
    matched_cmd: CliCommand = args.cmd
    matched_cmd.execute(vars(args))
