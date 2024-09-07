from typing import Dict
from gaidme.models import BaseCommand

class CommandManager:
    def __init__(self):
        self.commands: Dict[str, BaseCommand] = {}

    def add_command(self, name: str, command_instance: BaseCommand):
        self.commands[name] = command_instance

    def execute(self, command_name: str, *args, **kwargs):
        if command_name in self.commands:
            return self.commands[command_name].execute(*args, **kwargs)
        else:
            return f"Unknown command: {command_name}"

    def handle_input(self, user_input: str, *args, **kwargs):
        command = user_input.split()[0] if user_input else ""
        question = user_input[len(command)+1:]
        if command in self.commands:
            return self.execute(command, question=question, *args, **kwargs)
        else:
            return None  # Allow non-command input to be handled elsewhere

    def get_available_commands(self):
        return list(self.commands.keys())
