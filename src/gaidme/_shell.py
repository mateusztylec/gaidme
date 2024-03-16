from ._errors import GaidmeError
from shellingham import detect_shell, ShellDetectionFailure
from pathlib import Path
from typing import Any
import logging
import pexpect
import signal
import shutil
import sys
import os

_logger = logging.getLogger(__name__)


class Shell:
    _shell = None

    def __init__(self, name: str, path: str) -> None:
        self._name = name
        self._path = path
        _logger.debug(f"Detected {name} shell")

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @classmethod
    def get(cls):
        if cls._shell is not None:
            return cls._shell

        try:
            name, path = detect_shell(os.getpid())
        except (RuntimeError, ShellDetectionFailure):
            shell = None

            if os.name == "posix":
                shell = os.environ.get("SHELL")
            elif os.name == "nt":
                shell = os.environ.get("COMSPEC")

            if not shell:
                raise RuntimeError("Unable to detect the current shell")
            name, path = Path(shell).stem, shell

        cls._shell = cls(name, path)
        return cls._shell


    def execute(self, command: str) -> int:
        terminal = shutil.get_terminal_size()
        c = pexpect.spawnu(
            self._path, dimensions=(terminal.lines, terminal.columns))

        if self._name == "zsh":
            c.setecho(False)

        c.sendline(command)

        def resize(sig: Any, data: Any) -> None:
            terminal = shutil.get_terminal_size()
            c.setwinsize(terminal.lines, terminal.columns)

        signal.signal(signal.SIGWINCH, resize)

        c.interact(escape_character=None)
        c.close()

        sys.exit(c.exitstatus)

    def check_complience(self):
        if self._name == "bash":
            if os.getenv("PROMPT_COMMAND") != "history -a;":
                raise GaidmeError("Missing PROMPT_COMMAND env variable. Run `export 'PROMPT_COMMAND=history -a;'`")
        if self._name == "sh":
            raise GaidmeError("sh shell in not supported for 'reflect' command")
    

