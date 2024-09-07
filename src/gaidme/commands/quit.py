from gaidme.models import BaseCommand

class QuitCommand(BaseCommand):
    @property
    def description(self):
        return "Quit the application"

    def execute(self, *args, **kwargs):
        self.gaidme.io.print_message("Goodbye!")
        self.gaidme.running = False
