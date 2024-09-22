from gaidme.models import BaseCommand

class SettingsCommand(BaseCommand):
    @property
    def description(self):
        return "Change settings"

    def execute(self, *args, **kwargs) -> None:
        choices = ["Change API key", "Back to main menu"]
        selection = self.gaidme.io.choose_option(message="Settings", choices=choices)
        
        if selection == "Change API key":
            self.prompt_for_api_key()

    def prompt_for_api_key(self) -> None:
        api_key = self.gaidme.io.type_password("Please enter your GAIDME API key:")
        if api_key:
            self.gaidme.config_manager.save_api_key(api_key)
            self.gaidme.io.print_message("API key saved successfully.")
        else:
            self.gaidme.io.print_message("API key cannot be empty")
