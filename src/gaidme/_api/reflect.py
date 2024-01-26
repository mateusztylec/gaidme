from .._errors import display_warning
from .._tempfiles import TempFile
from .._shell import Shell
import logging
import os

_logger = logging.getLogger(__name__)

def reflect_command(args) -> None:
    """
    """
    user_query = ' '.join(args.reflect)
    TempFile.create('user_query.txt', user_query)

    shell = Shell.get()
    shell.check_complience()
    display_warning("This command will run previous command in the background. You have 4 sec to stop it")

    if os.getenv("GAIDME_DEV") == "True":
        shell.execute("""history | tail -n 2 | head -n 1 | awk '{$1=""; print substr($0, 2)}' > $(echo $GAIDME_BASE_DIR)/command.txt;echo "Will run: $(cat $(echo $GAIDME_BASE_DIR)/command.txt)"; sleep 4; source $(echo $GAIDME_BASE_DIR)/command.txt > $(echo $GAIDME_BASE_DIR)/command_result.txt; python -m gaidme.cli hidden""")
    shell.execute("""history | tail -n 2 | head -n 1 | awk '{$1=""; print substr($0, 2)}' > $(echo $GAIDME_BASE_DIR)/command.txt;echo "Will run: $(cat $(echo $GAIDME_BASE_DIR)/command.txt)"; sleep 4; source $(echo $GAIDME_BASE_DIR)/command.txt > $(echo $GAIDME_BASE_DIR)/command_result.txt; gaidme hidden""")


