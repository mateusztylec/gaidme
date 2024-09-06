from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers.shell import BashLexer
from prompt_toolkit.formatted_text import HTML
import questionary
from gaidme.config_manager import get_api_key, ConfigManager
from gaidme.logger import get_logger

logger = get_logger(__name__)

class GAIDME:
    def __init__(self):
        self.running = True
        self.command_history = []
        self.api_key = self.ensure_api_key()
        self.setup_prompt()

    def setup_prompt(self):
        # Only autocomplete the /ask command
        completer = WordCompleter(['/ask'], ignore_case=True)

        # Custom style
        style = Style.from_dict({
            'completion-menu.completion': 'bg:#008888 #ffffff',
            'completion-menu.completion.current': 'bg:#00aaaa #000000',
            'scrollbar.background': 'bg:#88aaaa',
            'scrollbar.button': 'bg:#222222',
        })

        # Bottom toolbar function
        def bottom_toolbar():
            return HTML('Type <b><style bg="ansiyellow">/ask</style></b> for AI assistance or <b><style bg="ansired">exit</style></b> to quit')

        self.session = PromptSession(
            history=InMemoryHistory(),
            completer=completer,
            lexer=PygmentsLexer(BashLexer),
            style=style,
            bottom_toolbar=bottom_toolbar,
            complete_while_typing=True
        )

    def ensure_api_key(self):
        api_key = get_api_key()
        if not api_key:
            print("GAIDME API key not found.")
            choice = questionary.select(
                "Choose an option:",
                choices=["Enter GAIDME API key"]
            ).ask()
            
            if choice == "Enter GAIDME API key":
                api_key = self.prompt_for_api_key()
            else:
                print("Cannot proceed without an API key. Exiting.")
                exit(1)
        
        return api_key

    def prompt_for_api_key(self):
        api_key = questionary.password("Please enter your GAIDME API key:").ask()
        if api_key:
            ConfigManager().save_api_key(api_key)
            print("API key saved successfully.")
        else:
            print("No API key entered. Cannot proceed. Exiting.")
            exit(1)
        return api_key

    def run(self):
        print("Welcome to GAIDME! Type 'exit' to quit. Use '/ask' for AI assistance.")
        while self.running:
            try:
                user_input = self.session.prompt("gaidme> ").strip()
                if user_input.lower() == 'exit':
                    self.running = False
                    print("Goodbye!")
                elif user_input.startswith("/ask "):
                    self.process_question(user_input[5:])
                else:
                    self.execute_command(user_input)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")

    def process_question(self, question):
        print(f"User asked: {question}")
        # Here you would integrate with your LLM to get a response
        print("AI: This is where the LLM would provide an answer.")

    def execute_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            rc = process.poll()
            error_output = process.stderr.read()
            if error_output:
                print("Errors:")
                print(error_output)
            self.command_history.append({"command": command, "result": error_output if rc != 0 else "Success"})
        except Exception as e:
            print(f"Error executing command: {e}")

def main():
    gaidme = GAIDME()
    gaidme.run()

if __name__ == "__main__":
    main()