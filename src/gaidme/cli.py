from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.shortcuts import CompleteStyle
import pyperclip
from gaidme.config_manager import get_api_key, ConfigManager
from gaidme.logger import get_logger
import subprocess
import sys
from gaidme.compiler import CustomCompleter
from gaidme.io import IO
from gaidme.commands import Commands

logger = get_logger(__name__)

class GAIDME:
    def __init__(self):
        self.running = True
        self.command_history = []
        self.history = InMemoryHistory()
        self.session = self.setup_prompt()
        self.io = IO()
        self.commands_handler = Commands()
        self.secret_manager = ConfigManager()

        self.ensure_api_key()

    def setup_prompt(self):
        style = Style.from_dict({
            'completion-menu.completion': 'bg:#008888 #ffffff',
            'completion-menu.completion.current': 'bg:#00aaaa #000000',
        })

        return PromptSession(
            history=InMemoryHistory(),
            completer=CustomCompleter(),
            style=style,
            complete_while_typing=True,
            editing_mode=EditingMode.EMACS,
            complete_style=CompleteStyle.MULTI_COLUMN,
            reserve_space_for_menu=4,
        )


    def ensure_api_key(self):
        api_key = get_api_key()
        if not api_key:
            self.io.print_message("GAIDME API key not found.")
            choice = self.io.choose_option(
                message="Choose an option:",
                choices=["Enter GAIDME API key"]
            )

            if choice == "Enter GAIDME API key":
                api_key = self.prompt_for_api_key()
            else:
                self.io.print_message("Cannot proceed without an API key. Exiting.")
                sys.exit(1)
        
        return api_key

    def prompt_for_api_key(self):
        api_key = self.io.type_password("Please enter your GAIDME API key:")
        if api_key:
            self.secret_manager.save_api_key(api_key)
            self.io.print_message("API key saved successfully.")
        else:
            self.io.print_message("No API key entered. Cannot proceed. Exiting.")
            sys.exit(1)
        return api_key

    def run(self):
        self.io.print_message("Welcome to GAIDME! Type '/quit' to quit. Use '/ask' for AI assistance.")
        while self.running:
            try:
                user_input = self.session.prompt(
                    "gaidme>"
                ).strip()
                if user_input.startswith("/"):
                    output = self.commands_handler.handle_command(
                        command=user_input,
                        command_history=self.command_history,
                        function_callback=self.execute_command
                    )
                    self.io.print_message(output)
                else:
                    self.execute_command(user_input)
            except KeyboardInterrupt:
                self.io.print_message("\nUse '/quit' to quit.")

    def handle_selection(self, selection, command):
        if selection == "Copy command to clipboard":
            pyperclip.copy(command)
            self.io.print_message("Command copied to clipboard")
        elif selection == "Explain command":
            # Implement explanation functionality
            self.io.print_message("Explanation: [Your explanation here]")
        elif selection == "Execute command":
            self.execute_command(command)
        elif selection == "Quit":
            self.io.print_message("Exiting...")
            self.running = False

    def execute_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
            
            stdout_lines = []
            stderr_lines = []

            # Handle stdout in real-time
            for line in process.stdout:
                line = line.strip()
                if line:
                    self.io.print_message(line)
                    stdout_lines.append(line)

            # Handle stderr
            for line in process.stderr:
                line = line.strip()
                if line:
                    self.io.print_message(line)
                    stderr_lines.append(line)

            process.wait()
            rc = process.returncode
            
            stdout = "\n".join(stdout_lines)
            stderr = "\n".join(stderr_lines)
            result = "Success" if rc == 0 else stderr

            self.command_history.append({
                "command": command,
                "stdout": stdout,
                "stderr": stderr,
                "result": result
            })
        except Exception as e:
            self.io.print_message(f"Error executing command: {e}")
            self.command_history.append({
                "command": command,
                "error": str(e),
                "result": "Error"
            })


def main():
    gaidme = GAIDME()
    gaidme.run()

if __name__ == "__main__":
    main()