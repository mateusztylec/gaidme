import os  # Added import for accessing current directory
from typing import Dict, Any  # Added for type hinting in Python 3.8

from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.history import InMemoryHistory
from gaidme.io import IO
from gaidme.logger import get_logger
from gaidme.compiler import CustomCompleter
from gaidme.config_manager import ConfigManager
from gaidme.command_manager import CommandManager
from gaidme.history_manager import HistoryManager
from gaidme.exceptions import CommandNotAllowedError, InvalidAPIKeyError, APIError, APIVersionError, UsageLimitExceededError
from gaidme.commands.ask import AskCommand
from gaidme.commands.quit import QuitCommand
from gaidme.commands.help import HelpCommand
from gaidme.commands.settings import SettingsCommand

logger = get_logger(__name__)

class GAIDME:
    def __init__(self):
        self.running = True
        self.io = IO()
        self.command_manager = CommandManager()
        self.config_manager = ConfigManager()
        self.history = InMemoryHistory()
        self.history_manager = HistoryManager()

        self.session = self.setup_prompt()

    def get_prompt_text(self) -> str:
        current_path = self.io.get_current_path()
        home = os.path.expanduser("~")
        if current_path == home:
            display_path = "~"
        elif current_path.startswith(home):
            display_path = f"~{current_path[len(home):]}"
        else:
            display_path = current_path
        return f"gaidme: {display_path}> "

    def setup_commands(self) -> None:
        self.command_manager.add_command("/ask", AskCommand(self))
        self.command_manager.add_command("/settings", SettingsCommand(self))
        self.command_manager.add_command("/quit", QuitCommand(self))
        self.command_manager.add_command("/help", HelpCommand(self))

    def setup_prompt(self) -> PromptSession:
        self.setup_commands()

        style = Style.from_dict({
            'completion-menu.completion': 'bg:#BA55D3 #ffffff',  # Light purple background
            # Slightly darker light purple for current selection
            'completion-menu.completion.current': 'bg:#9370DB #000000',
            'prompt': 'bold #FFE403'  # Lighter yellow for the prompt
        })

        return PromptSession(
            history=self.history,
            completer=CustomCompleter(
                self.command_manager.get_available_commands()),
            style=style,
            complete_while_typing=True,
            editing_mode=EditingMode.EMACS,
            complete_style=CompleteStyle.MULTI_COLUMN,
            reserve_space_for_menu=3,
            message=self.get_prompt_text()  # Changed to dynamic prompt
        )

    def run(self) -> None:
        self.io.print_message(
            "Welcome to gaidme! Type /help for available commands")
        while self.running:
            try:
                self.session.message = self.get_prompt_text()  # Update prompt dynamically
                user_input = self.session.prompt()
                if user_input.startswith("/"):
                    self.command_manager.handle_input(
                        user_input, command_history=self.history_manager.get_history())
                else:
                    command_result = self.io.execute_command(user_input)
                    if user_input != "":
                        self.history_manager.add_to_history(**command_result)
            except KeyboardInterrupt:
                self.io.print_message("\nUse '/quit' to quit.")
            except (CommandNotAllowedError, InvalidAPIKeyError, APIVersionError, APIError, UsageLimitExceededError) as e:
                self.io.print_error(str(e))
            except Exception as e:
                logger.error(f"An unexpected error occurred: {str(e)}")
                self.io.print_error(
                    "An unexpected error occurred. Please try again.")


def main() -> None:
    gaidme = GAIDME()
    gaidme.run()


if __name__ == "__main__":
    main()
