import cmd
import sys

class GAIDME(cmd.Cmd):
    prompt = 'gaidme> '
    intro = "Welcome to GAIDME! Type 'help' for a list of commands."

    def do_ask(self, arg):
        """Ask a question or give a command to the AI"""
        print(f"AI: You asked: {arg}")
        # Here you would typically send the question to an AI model and get a response

    def do_exit(self, arg):
        """Exit the application"""
        print("Goodbye!")
        return True

    def do_quit(self, arg):
        """Exit the application"""
        return self.do_exit(arg)

    def default(self, line):
        return self.do_ask(line)

def main():
    GAIDME().cmdloop()

if __name__ == "__main__":
    main()