from pydantic import BaseModel
from abc import ABC, abstractmethod

class CommandHistory(BaseModel):
    command: str
    stdout: str
    stderr: str
    result: str

class BaseCommand(ABC):
    def __init__(self, gaidme_instance):
        self.gaidme = gaidme_instance

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def description(self):
        pass