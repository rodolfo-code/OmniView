from abc import ABC, abstractmethod

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