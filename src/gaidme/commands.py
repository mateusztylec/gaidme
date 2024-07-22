from gaidme.api_client import get_ai_response
from gaidme.io import IO
import pyperclip
import sys

class Commands:
    _commands = ["/ask", "/quit", "/help", "/settings"]

    def __init__(self):
        self.io = IO()

    @staticmethod
    def available_commands():
        return Commands._commands
    
    def handle_command(self, command, command_history, function_callback):
        if command.startswith("/ask"):
            self.ask_command(command[5:], command_history, function_callback)
        elif command.startswith("/quit"):
            message: str = self.quit_command()
            self.io.print_message(message)
            sys.exit(0)
        elif command.startswith("/help"):
            return self.help_command()
        elif command.startswith("/settings"):
            return self.settings_command()
        else:
            return "Command not found"

    def ask_command(self, question, command_history, function_callback):
        ai_command = get_ai_response(question, command_history)
        self.io.print_ai_suggestion(ai_command)
        options = [
            "Run command",
            "Copy command",
            "Explain command",
            "Quit"
        ]
            
        selection = self.io.choose_option(
            message="Select an option",
            choices=options,
            instruction="[Use arrows to move, type to filter]"
        )
        
        if selection == "Copy command":
            pyperclip.copy(ai_command)
            self.io.print_message("Command copied to clipboard")
        elif selection == "Explain command":
            self.io.print_message("NOT IMPLEMENTED")
        elif selection == "Run command":
            function_callback(ai_command)
        elif selection == "Quit":
            self.io.print_message("Quitting...")
            sys.exit(0)

    def quit_command(self):
        return "Goodbye!"
    
    def help_command(self):
        return "Help command TODO"
    
    def settings_command(self):
        return "Settings command TODO"

    @staticmethod
    def get_completions(cmd):
        # Add command-specific completions here
        completions = {
            'ask': ['question', 'help'],
            'reflect': ['previous', 'all'],
            'copy': ['last', 'all'],
            'exit': []
        }
        return completions.get(cmd, [])