from ._errors import GaidmeError, CLIError, display_error
from ._api.reflect import reflect_command
from ._api.hidden import hidden_command
from ._version import __version__
from ._api.ask import ask_command
from argparse import Namespace
import argparse
import pydantic
import logging
import sys

_logger = logging.getLogger("gaidme.cli")

def main() -> int:
    try:
        _main()
    except (GaidmeError, CLIError, pydantic.ValidationError) as err:
        display_error(err)
        return 1
    except KeyboardInterrupt:
        sys.stderr.write("\n")
        return 1
    return 0


def _main() -> None:
    parser = _parser_build()
    args = _parse_args(parser)

    if args.verbosity != 0:
        sys.stderr.write("Warning: --verbosity isn't supported yet\n")

    args.func(args)

    
def _parse_args(parser: argparse.ArgumentParser) -> Namespace:
    args = parser.parse_args()
    _logger.debug("Parsing successful")
    _logger.debug(f"{args}")
    return args


def _parser_build() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gaidme")

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbosity",
        default=0,
        help="Set verbosity level"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s"+__version__,
    )

    subparsers = parser.add_subparsers()
    parser_ask = subparsers.add_parser(
        "ask", help="Ask ai about specific command")
    parser_ask.add_argument(
        "ask", nargs="*", help="Ask ai about specific command")
    parser_ask.set_defaults(func=ask_command)

    parser_reflect = subparsers.add_parser(
        "reflect", help="Reflet about previous command")
    parser_reflect.add_argument(
        "reflect", nargs="*", help="Reflect about previous command")
    parser_reflect.set_defaults(func=reflect_command)

    parser_hidden = subparsers.add_parser(
        "hidden")
    parser_hidden.set_defaults(func=hidden_command)

    def help(param) -> None:
        parser.print_help()

    parser.set_defaults(func=help)
    return parser


if __name__ == "__main__":
    main()
