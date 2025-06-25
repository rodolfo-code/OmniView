from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from app.domain.person import Person
from app.domain.task import Task

class DeltaTaskRequester(BaseModel):
    name: str
    email: str
    avatar: Optional[str] = ""

class DeltaTask(BaseModel):
    title: str
    description: str
    client: str
    contract: Optional[str] = None
    status: Optional[str] = None
    requester: Optional[Person] = None
    responsible: Optional[Person] = None
    createdAt: Optional[str] = None

    @classmethod
    def from_task(cls, task: Task) -> dict:
        return cls(
            title=task.title,
            description=task.description,
            client=task.client,
            contract=None,  
            status="Aguardando Início",
            requester=Person(
                name=task.sender,
                email=task.sender_email
            ),
            responsible=Person(
                name=task.responsible,
                email=task.responsible_email
            ),
            createdAt=datetime.now().isoformat() # formato de saida = 2025-06-19T11:38:19.000000
        )
    
    def to_api_format(self) -> dict:
        """Converte para o formato esperado pela API"""
        return self.model_dump(exclude_none=True)