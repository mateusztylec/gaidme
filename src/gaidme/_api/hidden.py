from ..schema import reflect_system_promt
from .._terminal import _print_command
from ..utils import _get_hidden_args
from ..models import get_reflection
import logging

_logger = logging.getLogger(__name__)

def hidden_command(args):
    """
    Executes a hidden command based on previously stored arguments.
    
    This function retrieves command arguments from temporary files, constructs a system prompt,
    and then executes a reflection based on the user query and system prompt.
    """
    files_content = _get_hidden_args()
    system_prompt = reflect_system_promt(files_content['command'], files_content['command_result'])

    result = get_reflection(files_content['user_query'], system_prompt)
    _print_command(result)