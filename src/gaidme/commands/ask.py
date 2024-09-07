from gaidme.models import BaseCommand
from gaidme.api_client import get_ai_response
import pyperclip

class AskCommand(BaseCommand):
    @property
    def description(self):
        return "Ask AI for assistance"

    def execute(self, *args, **kwargs):
        
        ai_command = get_ai_response(question=kwargs.get('question'), command_history=self.gaidme.history_manager.get_history())
        self.gaidme.io.print_ai_suggestion(ai_command)
        
        options = ["Run command", "Copy command", "Explain command", "Back to main menu"]
        selection = self.gaidme.io.choose_option(message="Select an option", choices=options)
        
        if selection == "Run command":
            self.gaidme.io.execute_command(ai_command)
        elif selection == "Copy command":
            pyperclip.copy(ai_command)
            self.gaidme.io.print_message("Command copied to clipboard")
        elif selection == "Explain command":
            # Implement explanation functionality
            self.gaidme.io.print_message("Explanation: [Your explanation here]")
