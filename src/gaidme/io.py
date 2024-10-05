import os  # Ensure os is imported for directory operations
import platform
from rich.console import Console
from rich.text import Text
import subprocess
import questionary
from questionary import Style
from gaidme.logger import get_logger
from gaidme.exceptions import CommandNotAllowedError
from gaidme.theme import gaidme_theme

logger = get_logger(__name__)

class IO:
    def __init__(self):
        self.console = Console(color_system="auto", theme=gaidme_theme)
        self.blacklisted_commands = []  # Remove interactive commands from blacklist
        self.interactive_commands = ['nano', 'vim', 'neovim', 'vi', 'emacs', 'ssh']
        self.current_path = os.getcwd()  # Initialize current_path

    def get_current_path(self) -> str:
        return self.current_path

    def set_current_path(self, path: str) -> None:
        self.current_path = path

    def print_message(self, message: str) -> None:
        self.console.print(message)

    def print_error(self, message: str) -> None:
        self.console.print(Text(message, style="bold red"))

    def choose_option(self, **kwargs):
        custom_style = Style.from_dict({
            'question': 'fg:#BA55D3',  # question after ? sign
            'answer': 'fg:#FFE403',    # answer in options
            'pointer': 'fg:#FFE403',   # pointer in options in the left
            'highlighted': 'fg:#FFE403',  # selected in options
            'qmark': 'fg:#BA55D3',     # ? sign
            'selected': 'fg:#cc5454',
            'separator': 'fg:#F11144',
            'instruction': 'fg:#9370DB',  # (user arrows)
        })
        return questionary.select(**kwargs, style=custom_style).ask()
    
    def type_password(self, text: str):
        custom_style = Style.from_dict({
            'qmark': 'fg:#BA55D3 bold',      # ? sign
            'answer': 'fg:#FFE403 bold',     # *** in password
            'question': 'fg:#BA55D3 bold',   # question after ? sign
        })
        return questionary.password(text, style=custom_style).ask()
    
    def print_ai_suggestion(self, suggestion: str) -> None:
        styled_message = Text()
        styled_message.append("Suggestion: ", style="#BA55D3")
        styled_message.append(suggestion, style="bold italic #FFE403")
        self.console.print(styled_message)

    def execute_command(self, command: str):
        command = command.strip()
        if not command:
            return {
                "command": "",
                "stdout": "",
                "stderr": "",
            }

        # Handle 'cd' internally
        if command.startswith("cd"):
            parts = command.split(maxsplit=1)
            if len(parts) == 1:
                # No argument, go to home directory
                path = os.path.expanduser("~")
            else:
                path = parts[1].strip()
                # Expand user (~) and variables
                path = os.path.expanduser(path)
                path = os.path.expandvars(path)

            # Resolve the new path relative to current_path
            new_path = os.path.join(self.current_path, path) if not os.path.isabs(path) else path

            # Normalize the path
            new_path = os.path.abspath(new_path)

            try:
                if os.path.isdir(new_path):
                    self.current_path = new_path
                    return {
                        "command": "cd",
                        "stdout": f"Changed directory to {self.current_path}",
                        "stderr": ""
                    }
                else:
                    error_message = f"cd: no such file or directory: {path}"
                    self.print_error(error_message)
                    logger.error(error_message)
                    return {
                        "command": "cd",
                        "stdout": "",
                        "stderr": error_message
                    }
            except PermissionError:
                error_message = f"cd: permission denied: {path}"
                self.print_error(error_message)
                logger.error(error_message)
                return {
                    "command": "cd",
                    "stdout": "",
                    "stderr": error_message
                }
            except Exception as e:
                error_message = f"cd: {str(e)}"
                self.print_error(error_message)
                logger.error(error_message)
                return {
                    "command": "cd",
                    "stdout": "",
                    "stderr": error_message
                }

        # Existing handling for other commands
        # Check if the command is blacklisted
        if any(command.startswith(cmd) for cmd in self.blacklisted_commands):
            blocked_command = next(cmd for cmd in self.blacklisted_commands if command.startswith(cmd))
            error_message = f"Command '{blocked_command}' is not allowed."
            raise CommandNotAllowedError(error_message)

        # Check if the command is interactive
        is_interactive = any(command.startswith(cmd) for cmd in self.interactive_commands)

        try:
            # Determine shell usage based on the operating system
            if platform.system() == "Windows":
                shell = True  # Use shell=True on Windows to access built-in commands like 'dir'
            else:
                shell = False  # Use shell=False on Unix-like systems for security

            if is_interactive:
                # Execute interactive command with shell=True
                logger.debug(f"Executing interactive command: {command}")
                process = subprocess.Popen(command, shell=True, cwd=self.current_path)
                process.communicate()
                rc = process.returncode
                return {
                    "command": command,
                    "stdout": "",
                    "stderr": ""
                }
            else:
                # Non-interactive command: capture stdout and stderr
                # Parse the command using shlex for security

                process = subprocess.Popen(
                    command,
                    shell=True,  # Use shell=False on Unix-like systems
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    cwd=self.current_path  # Set the current working directory
                )
                
                stdout_lines = []
                stderr_lines = []

                # Handle stdout in real-time
                for line in process.stdout:
                    line = line.rstrip()  # Remove trailing newline
                    if line:
                        self.print_message(line)
                        stdout_lines.append(line)

                # Handle stderr
                for line in process.stderr:
                    line = line.rstrip()  # Remove trailing newline
                    if line:
                        self.print_error(line)
                        stderr_lines.append(line)

                process.wait()
                rc = process.returncode
                
                stdout = "\n".join(stdout_lines)
                stderr = "\n".join(stderr_lines)

                return {
                    "command": command,
                    "stdout": stdout,
                    "stderr": stderr
                }
        except Exception as e:
            error_message = f"Error executing command: {e}"
            self.print_error(error_message)
            logger.error(error_message)
            return {
                "command": command,
                "stdout": "",
                "stderr": error_message
            }