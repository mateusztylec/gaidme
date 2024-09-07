from gaidme.models import BaseCommand
from gaidme.api_client import get_ai_response
from gaidme.config_manager import ConfigError
import pyperclip

class AskCommand(BaseCommand):
    @property
    def description(self):
        return "Ask AI for assistance"

    def execute(self, *args, **kwargs):
        
        try:
            ai_command = get_ai_response(question=kwargs.get('question'), history_manager=self.gaidme.history_manager, config_manager=self.gaidme.config_manager)
        except ConfigError as e:
            self.gaidme.io.print_error(str(e))
            
        self.gaidme.io.print_ai_suggestion(ai_command)
        
        choices = ["Run command", "Copy command", "Explain command", "Back to main menu"]
        selection = self.gaidme.io.choose_option(message="Select an option", choices=choices)
        
        if selection == "Run command":
            command_details = self.gaidme.io.execute_command(ai_command)
            self.gaidme.history_manager.add_to_history(**command_details)
        elif selection == "Copy command":
            pyperclip.copy(ai_command)
            self.gaidme.io.print_message("Command copied to clipboard")
        elif selection == "Explain command":
            # Implement explanation functionality
            self.gaidme.io.print_message("Explanation: [Your explanation here]")
