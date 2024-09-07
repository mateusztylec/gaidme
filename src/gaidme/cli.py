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
from gaidme.exceptions import CommandNotAllowedError
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

    def setup_commands(self):
        self.command_manager.add_command("/ask", AskCommand(self))
        self.command_manager.add_command("/settings", SettingsCommand(self))
        self.command_manager.add_command("/quit", QuitCommand(self))
        self.command_manager.add_command("/help", HelpCommand(self))

    def setup_prompt(self):
        self.setup_commands()

        style = Style.from_dict({
            'completion-menu.completion': 'bg:#008888 #ffffff',
            'completion-menu.completion.current': 'bg:#00aaaa #000000',
        })

        return PromptSession(
            history=self.history,
            completer=CustomCompleter(self.command_manager.get_available_commands()),
            style=style,
            complete_while_typing=True,
            editing_mode=EditingMode.EMACS,
            complete_style=CompleteStyle.MULTI_COLUMN,
            reserve_space_for_menu=3
        )

    def run(self):
        self.io.print_message("Welcome to GAIDME! Type '/help' for available commands.")
        while self.running:
            try:
                user_input = self.session.prompt(
                    "gaidme> ",
                    style=Style.from_dict({
                        'prompt': 'bold #ffff00',  # Yellow color for the prompt
                    })
                ).strip()
                if user_input.startswith("/"):
                    self.command_manager.handle_input(user_input, command_history=self.history_manager.get_history())
                else:
                    command_result = self.io.execute_command(user_input)
                    self.history_manager.add_to_history(**command_result)
            except KeyboardInterrupt:
                self.io.print_message("\nUse '/quit' to quit.")
            except CommandNotAllowedError as e:
                self.io.print_error(str(e))

def main():
    gaidme = GAIDME()
    gaidme.run()

if __name__ == "__main__":
    main()