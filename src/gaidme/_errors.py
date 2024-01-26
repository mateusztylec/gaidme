import sys

class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class GaidmeError(Exception):
    pass

class CLIError(GaidmeError):
    ...

def display_error(err: GaidmeError) -> None:
    sys.stderr.write("{}Error:{} {}\n".format(Colors.FAIL, Colors.ENDC, err))

def display_warning(war: str) -> None:
    sys.stdout.write("{}Warning:{} {}\n".format(Colors.WARNING, Colors.ENDC, war))