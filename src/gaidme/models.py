from .schema import get_command_fnc, get_command_system_prompt
from .utils import _parse_command_from_response
from ._errors import GaidmeError
from openai import OpenAI, AzureOpenAI
from typing import Union
import logging
import os

_logger = logging.getLogger(__name__)

def get_ai_client_and_model() -> Union[list[AzureOpenAI, str], list[OpenAI, str]]:
    """
    Based on the env variable returns openai client.
    It is ugly and will be refactored later
    """
    if os.getenv("OPENAI_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY")), os.getenv("OPENAI_API_MODEL")
    elif os.getenv("AZURE_OPENAI_ENDPOINT"):
        if not os.getenv("AZURE_OPENAI_KEY"):
            raise GaidmeError("Missing AZURE_OPENAI_KEY")
        if not os.getenv("AZURE_OPENAI_DEPLOYMENT"):
            raise GaidmeError("Missing AZURE_OPENAI_DEPLOYMENT")
        if not os.getenv("AZURE_OPENAI_API_VERSION"):
            return AzureOpenAI(azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                            api_key=os.getenv("AZURE_OPENAI_KEY")), os.getenv("AZURE_OPENAI_DEPLOYMENT")
        else:
            return AzureOpenAI(azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                               api_key=os.getenv("AZURE_OPENAI_KEY"),
                               api_version=os.getenv("AZURE_OPENAI_API_VERSION")), os.getenv("AZURE_OPENAI_DEPLOYMENT")
             
    else:
        raise GaidmeError("Missing OPENAI_API_KEY")

def get_command(user_prompt: str) -> str:
    client, model = get_ai_client_and_model()
    _logger.debug("running get_command")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": get_command_system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        tools=[get_command_fnc],
        tool_choice={"type": "function", "function": {
            "name": get_command_fnc['function']['name']}}
    )
    command = _parse_command_from_response(response)

    return command

def get_reflection(user_prompt: str, system_prompt: str) -> str:
    client, model = get_ai_client_and_model()
    _logger.debug("running get_reflection")
    _logger.debug(system_prompt)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        tools=[get_command_fnc],
        tool_choice={"type": "function", "function": {
            "name": get_command_fnc['function']['name']}}
    )
    command = _parse_command_from_response(response)

    return command


def moderation(prompt: str) -> None:
    """
    Use openai moderation endpoint.
    Not in used currently
    """
    client, model = get_ai_client_and_model()
    mod_response = client.moderations.create(input=prompt)
    if mod_response.results[0].flagged is True:
        raise GaidmeError("This message has been flagged as harmful by OpenAI")
