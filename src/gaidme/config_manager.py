import os
import json
from pathlib import Path
from gaidme.exceptions import ConfigError

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.gaidme'
        self.config_file = self.config_dir / 'config.json'
        self.ensure_config_dir()
        self._config = self._load_config()

    def ensure_config_dir(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def get_api_key(self) -> str:
        api_key = self._config.get("api_key")
        if not api_key:
            raise ConfigError("API key was not found")
        return api_key

    def save_api_key(self, api_key: str) -> None:
        self._config["api_key"] = api_key
        self._save_config()

    def _load_config(self) -> dict:
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                return json.load(f)
        else:
            self._create_config()
        return {}
    
    def _create_config(self) -> None:
        self._config = {
            "api_key": ""
        }
        self._save_config()

    def _save_config(self) -> None:
        with open(self.config_file, "w") as f:
            json.dump(self._config, f)

    def clear_config(self) -> None:
        self._config = {}
        self._save_config()

    def update_config(self, new_config: dict) -> None:
        self._config.update(new_config)
        self._save_config()

