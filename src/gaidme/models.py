from pydantic import BaseModel

class CommandHistory(BaseModel):
    command: str
    stdout: str
    stderr: str
    result: str