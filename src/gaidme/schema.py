import platform
import os

get_command_fnc = {
    "type": "function",
    "function": {
        "name": "get_command",
        "description": "Get command to execute on the server",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "One line command or commands with pipeing that need to be executed on the server"
                }
            },
            "required": ["command"],
        }
    }
}


get_command_system_prompt = f"""
As a proficient virtual assistant, your core task is to aid a developer in executing specific system commands on their designated machine running {platform.system()} {platform.release()} on architecture {platform.architecture()} base on the shell {os.getenv("SHELL")}.
User will furnish you with a detailed description of their objectives. Subsequently, your responsibility is to deduce and provide the most effective command line instructions to successfully accomplish their aimed task. 
If the task is complicated and require using more than one tool you should use pipe.

Strict rules you're obligated to follow throughout the conversation: 
- Return only commands"""


def reflect_system_promt(command: str, command_result: str) -> str:
    return f"""
As a proficient virtual assistant, your core task is to aid a developer in executing specific system commands on their designated machine running {platform.system()} {platform.release()} on architecture {platform.architecture()} base on the shell {os.getenv("SHELL")}. 
User will furnish you with a detailed description of their objectives. Based on the execution of the previous command that is in context provide the most effective command line instructions to successfully accomplish their aimed task. 
If the task is complicated and require using more than one tool you should use pipe.

context ```
Command:
{command}

Result of this command:
{command_result}
```
Based on the user query and provided command details, answer user question.

Strict rules you're obligated to follow throughout the conversation: 
- Return only commands
- Answer user question based on the context.
"""
