from .._terminal import _print_command
from ..models import get_command
import logging

_logger = logging.getLogger(__name__)

def ask_command(args):
    commands = get_command(' '.join(args.ask))
    _print_command(commands)