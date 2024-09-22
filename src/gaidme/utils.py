import platform
import os

def get_system_metadata():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "terminal": os.environ.get("TERM", "Unknown"),
        "shell": os.environ.get("SHELL", "Unknown")
    }