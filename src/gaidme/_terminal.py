from ._shell import Shell
import readline

def _prefill_with_command(command: str) -> None:
    def hook() -> None:
        readline.insert_text(command)
        readline.redisplay()
    readline.set_pre_input_hook(hook)

def _print_command(command: str) -> None:
    _prefill_with_command(command)

    modified_command = input("")
    readline.set_pre_input_hook(None)

    shell = Shell.get()
    shell.execute(modified_command)