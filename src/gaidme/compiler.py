from prompt_toolkit.completion import Completer, Completion
from typing import List

class CustomCompleter(Completer):
    def __init__(self, commands: List[str]):
        self.command_names = commands
        self.command_completions = {}

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        if not words:
            return

        if text[0] == "/":
            if len(words) == 1 and not text[-1].isspace():
                partial = words[0]
                candidates = self.command_names
                for cmd in candidates:
                    if cmd.startswith(partial):
                        yield Completion(cmd, start_position=-len(partial))
            return