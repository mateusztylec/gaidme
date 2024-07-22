from rich.console import Console
from prompt_toolkit.styles import Style
import questionary

class IO:
    def __init__(self):
        self.console = Console(color_system=None)

    def print_message(self, message):
        self.console.print(message)

    def choose_option(self, **kwargs):
        custom_style = Style([
            ('question', 'fg:#673ab7 bold'),
            ('answer', 'fg:#f44336 bold'),
            ('pointer', 'fg:#673ab7 bold'),
            ('highlighted', 'fg:#673ab7 bold'),
            ('selected', 'fg:#cc5454'),
            ('separator', 'fg:#673ab7'),
            ('instruction', 'fg:#0d47a1'),
        ])
        return questionary.select(**kwargs, style=custom_style).ask()
    
    def type_password(self, text: str):
        return questionary.password(text).ask()
    
    def print_ai_suggestion(self, suggestion):
        self.console.print(f"Suggestion: {suggestion}")