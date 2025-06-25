from abc import ABC, abstractmethod
from typing import Sequence

from langchain_core.messages import BaseMessage

class ILLMService(ABC):
    @abstractmethod
    def classify_email(self, email: str) -> str:
        '''
        Classifica o e-mail em uma categoria.
        '''
        pass

    @abstractmethod
    def extract_tasks(self, email: str) -> list[str]:
        '''
        Extrai as tarefas do e-mail.
        '''
        pass

    @abstractmethod
    def client_tools(self, messages: Sequence[BaseMessage]):
        """
        Chama a ferramenta de inserção de tarefas.
        """	
        pass
