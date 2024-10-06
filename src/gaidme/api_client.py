import requests
from requests import Response
from gaidme.history_manager import HistoryManager
from gaidme.config_manager import ConfigManager
from gaidme.exceptions import InvalidAPIKeyError, APIError, UsageLimitExceededError
from gaidme._version import __version__ as client_version
from gaidme.utils import get_system_metadata
from gaidme.logger import get_logger
logger = get_logger(__name__)

def extract_error_details(response: Response):
    """
    Extract status code and error details from the API response.
    
    Args:
        response (requests.Response): The API response object.
    
    Returns:
        tuple: A tuple containing (status_code, error_code, error_message).
    """
    status_code = response.status_code
    logger.debug(f"Status code: {status_code}")
    try:
        logger.debug(f"Response: {response.json()}")
        error_data = response.json().get("error", {})
        logger.debug(f"Error data: {error_data}")
        error_code = error_data.get("type", "unknown_error")
        error_message = error_data.get("message", "An unknown error occurred")
    except ValueError as e:
        logger.debug(f"{e}")
        error_code = "invalid_json"
        error_message = "Invalid JSON response from API"
    
    return status_code, error_code, error_message

def handle_api_error(response):
    """Handle API errors and raise appropriate exceptions."""
    if not response.ok:
        status_code, error_code, error_message = extract_error_details(response)
        if status_code == 401 and error_code == "invalid_api_key":
            raise InvalidAPIKeyError("Invalid API key")
        elif status_code == 429 and error_code == "usage_limit_exceeded":
            raise UsageLimitExceededError("Usage limit exceeded. Check your usage at https://gaidme.app/dashboard/usage")
        elif status_code == 502:
            raise APIError("Service is under maintenance. Please try again later.")
        else:
            raise APIError(f"API request failed: {error_message}")

def get_ai_response(question: str, history_manager: HistoryManager, config_manager: ConfigManager):
    api_key = config_manager.get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Client-Version": client_version
    }
    payload = {
        "question": question,
        "command_history": [command for command in history_manager.get_history()],
        "metadata": {
            "system": get_system_metadata()
        }
    }

    api_url = "https://api.gaidme.app"
    logger.debug(f"Sending request to {api_url}")

    try:
        response = requests.post(
            f"{api_url}/v1/completions/asks",
            json=payload,
            headers=headers,
            timeout=12
        )
        handle_api_error(response)
        return response.json()["answer"]
    except requests.exceptions.Timeout:
        raise APIError("The request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        raise APIError(f"API request failed: {str(e)}")
