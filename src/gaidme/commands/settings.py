from gaidme.models import BaseCommand

class SettingsCommand(BaseCommand):
    @property
    def description(self):
        return "Change settings"

    def execute(self, *args, **kwargs):
        options = ["Change API key", "Back to main menu"]
        selection = self.gaidme.io.choose_option("Settings", options)
        
        if selection == "Change API key":
            self.gaidme.prompt_for_api_key()
