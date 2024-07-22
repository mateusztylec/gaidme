import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.gaidme'
        self.config_file = self.config_dir / 'config.json'
        self.ensure_config_dir()

    def ensure_config_dir(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save_api_key(self, api_key):
        config = {'gaidme_api_key': api_key}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def get_api_key(self):
        if not self.config_file.exists():
            return None
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        return config.get('gaidme_api_key')

def get_api_key():
    config_manager = ConfigManager()
    return config_manager.get_api_key()