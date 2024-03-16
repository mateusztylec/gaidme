from ._tempfiles import TempFile
from openai.types import Completion
import json
import os

def _parse_command_from_response(response: Completion) -> str:
    arguments = json.loads(
        response.choices[0].message.tool_calls[0].function.arguments)
    return arguments['command']

        
def _get_hidden_args():
    """
    Retrieves content from temporary files.
    """
    filenames = ["user_query.txt", "command_result.txt", "command.txt"]
    files_content = {}
    for filename in filenames:
        # get rid of .txt suffix
        files_content[filename[:-4]] = TempFile.read(filename)
    
    if os.getenv("GAIDME_DEV") != "True":
        TempFile.cleanup()
    return files_content
