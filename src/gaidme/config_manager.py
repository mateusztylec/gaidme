import os
import json
from pathlib import Path

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.config_dir = Path.home() / '.gaidme'
        self.config_file = self.config_dir / 'config.json'
        self.ensure_config_dir()
        self._config = None

    def ensure_config_dir(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def get_api_key(self):
        if self._config is None:
            self._load_config()
        return self._config.get("api_key") or os.getenv("GAIDME_API_KEY")

    def save_api_key(self, api_key):
        self._config = {"api_key": api_key}
        with open(self.config_file, "w") as f:
            json.dump(self._config, f)

    def _load_config(self):
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                self._config = json.load(f)
        else:
            self._config = {}

config_manager = ConfigManager()