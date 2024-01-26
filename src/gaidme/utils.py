from ._errors import GaidmeError, CLIError
from ._tempfiles import TempFile
from openai.types import Completion
from typing import List
import json
import os

def _parse_command_from_response(response: Completion) -> str:
    arguments = json.loads(
        response.choices[0].message.tool_calls[0].function.arguments)
    return arguments['command']


# def load_env() -> None:
#     """
#     Required OPENAI_API_KEY
#     If OPENAI_API_KEY is missing we check for AZURE_OPENAI_API_KEY
#     If AZURE_OPENAI_API_KEY is missing we raise error
#     If AZURE_OPENAI_API_KEY is present we look for AZURE_OPENAI_ENDPOINT
#     If AZURE_OPENAI_ENDPOINT is not present 
#     If OPENAI_API_MODEL is empty we set this
#     """
#     if chat_
#     chat_model = os.getenv("OPENAI_API_MODEL")

#     if not chat_model:
#         os.environ["OPENAI_API_MODEL"] = "gpt-4-turbo-preview"
#     else:
#         if chat_model[4:5] == '3':
#             raise GaidmeError("Only GPT-4 and higher can be used")

#     if not os.getenv("OPENAI_API_KEY"):
#         if not os.getenv("AZURE_OPENAI_API_KEY"):
#             raise GaidmeError("Missing OpenAI API Key")
#         if not os.getenv("AZURE_OPENAI_ENDPOINT"):
#             raise GaidmeError("Missing Azure OpenAI Endpint")
        
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
