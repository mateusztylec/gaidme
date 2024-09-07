from rich.console import Console
from prompt_toolkit.styles import Style
import questionary
import subprocess
from gaidme.logger import get_logger

logger = get_logger(__name__)

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

    def execute_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
            
            stdout_lines = []
            stderr_lines = []

            # Handle stdout in real-time
            for line in process.stdout:
                line = line.strip()
                if line:
                    self.print_message(line)
                    stdout_lines.append(line)

            # Handle stderr
            for line in process.stderr:
                line = line.strip()
                if line:
                    self.print_message(line)
                    stderr_lines.append(line)

            process.wait()
            rc = process.returncode
            
            stdout = "\n".join(stdout_lines)
            stderr = "\n".join(stderr_lines)
            result = "Success" if rc == 0 else stderr

            return {
                "command": command,
                "stdout": stdout,
                "stderr": stderr,
                "result": result
            }
        except Exception as e:
            error_message = f"Error executing command: {e}"
            self.print_message(error_message)
            logger.error(error_message)
            return {
                "command": command,
                "stdout": "",
                "stderr": error_message,
                "result": "Error"
            }