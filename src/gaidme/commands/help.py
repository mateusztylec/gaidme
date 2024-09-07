from gaidme.models import BaseCommand

class HelpCommand(BaseCommand):
    @property
    def description(self):
        return "Show available commands"

    def execute(self, *args, **kwargs):
        self.gaidme.io.print_message("Available commands:")
        for command, instance in self.gaidme.command_manager.commands.items():
            self.gaidme.io.print_message(f"  {command}: {instance.description}")
