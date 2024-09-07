import requests
import platform
import os
from gaidme.models import CommandHistory
from gaidme.history_manager import HistoryManager
from gaidme.config_manager import ConfigManager

def get_system_metadata():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "terminal": os.environ.get("TERM", "Unknown"),
        "shell": os.environ.get("SHELL", "Unknown")
    }

def get_ai_response(question: str, history_manager: HistoryManager, config_manager: ConfigManager):
    api_key = config_manager.get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "question": question,
        "command_history": [command for command in history_manager.get_history()],
        "metadata": {
            "system": get_system_metadata()
        }
    }

    try:
        api_url = "https://api-dev.gaidme.app"
        # api_url = "http://localhost:5050"
        response = requests.post(f"{api_url}/v1/completions/asks", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["answer"]
    except requests.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")