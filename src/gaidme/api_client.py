import requests
import platform
import os
from gaidme.models import CommandHistory
from gaidme.config_manager import get_api_key

def get_system_metadata():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "terminal": os.environ.get("TERM", "Unknown"),
        "shell": os.environ.get("SHELL", "Unknown")
    }

def get_ai_response(question, command_history: list[CommandHistory]):
    api_key = get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "question": question,
        "command_history": [command for command in command_history],
        "metadata": {
            "system": get_system_metadata()
        }
    }

    try:
        response = requests.post("http://localhost:5050/v1/completions/asks", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["answer"]
    except requests.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")