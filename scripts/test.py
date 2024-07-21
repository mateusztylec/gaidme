import os
import sys
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

class GAIDME:
    def __init__(self):
        self.running = True
        self.command_history = []
        self.history = InMemoryHistory()
        self.session = PromptSession(history=self.history)

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