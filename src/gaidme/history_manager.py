from typing import List, Dict, Optional
from gaidme.logger import get_logger

logger = get_logger(__name__)

class HistoryManager:
    def __init__(self):
        self.command_history: List[Dict] = []
        self.total_history_chars = 0
        self.max_history_chars = 30000
        self.max_history_entries = 10
        self.truncated_entry_size = 500
        self.max_single_entry_chars = 3000

    def add_to_history(self, command: str, stdout: str, stderr: str, user_query: Optional[str] = None) -> None:
        def truncate(text: str, max_length: int):
            return (text[:max_length] + "...", True) if len(text) > max_length else (text, False)

        stdout, stdout_truncated = truncate(stdout, self.max_single_entry_chars)
        stderr, stderr_truncated = truncate(stderr, self.max_single_entry_chars)

        truncated = stdout_truncated or stderr_truncated
        if truncated:
            logger.debug("Command output truncated")
        
        new_entry = {
            "command": command,
            "stdout": stdout,
            "stderr": stderr,
            "truncated": stderr_truncated or stdout_truncated
        }
        if user_query is not None:
            new_entry["user_query"] = user_query

        # Calculate the size of the new entry
        entry_size = sum(len(v) for v in new_entry.values() if isinstance(v, str))

        # Add the new entry
        self.command_history.append(new_entry)
        self.total_history_chars += entry_size

        # Truncate older entries if necessary
        self._truncate_history()

    def _truncate_history(self) -> None:
        while self.total_history_chars > self.max_history_chars or len(self.command_history) > self.max_history_entries:
            if len(self.command_history) > 1:  # Ensure we always keep at least one entry
                oldest_entry = self.command_history[0]
                original_size = sum(len(v) for v in oldest_entry.values() if isinstance(v, str))
                
                # Truncate the oldest entry
                oldest_entry['stdout'] = oldest_entry['stdout'][:self.truncated_entry_size // 2] + "..."
                oldest_entry['stderr'] = oldest_entry['stderr'][:self.truncated_entry_size // 2] + "..."
                oldest_entry['truncated'] = True

                new_size = sum(len(v) for v in oldest_entry.values() if isinstance(v, str))
                self.total_history_chars -= (original_size - new_size)

                # If still over the limit, remove the oldest entry
                if self.total_history_chars > self.max_history_chars or len(self.command_history) > self.max_history_entries:
                    removed_entry = self.command_history.pop(0)
                    self.total_history_chars -= new_size
            else:
                # If we only have one entry and it's still too large, truncate it
                self.command_history[0]['stdout'] = self.command_history[0]['stdout'][:self.truncated_entry_size // 2] + "..."
                self.command_history[0]['stderr'] = self.command_history[0]['stderr'][:self.truncated_entry_size // 2] + "..."
                self.command_history[0]['truncated'] = True
                self.total_history_chars = sum(len(v) for v in self.command_history[0].values() if isinstance(v, str))
                break

    def get_history(self) -> List[Dict]:
        return self.command_history
