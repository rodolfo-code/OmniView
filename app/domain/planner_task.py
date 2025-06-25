from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from app.domain.task import Task

class CompanyCategory(Enum):
    VALE = "category1"
    ALLOS = "category2"
    EXTERNO = "category3"
    INTEGRIDADE = "category17"
    
    @classmethod
    def get_category(cls, company_name: str) -> Optional[str]:
        try:
            return cls[company_name.upper()].value
        except KeyError:
            return None

class PlannerTask(BaseModel):
    title: str
    description: str
    client: str
    contract: str
    responsible_email: str
    requester_email: str
    created_at: Optional[str] = None
    status: Optional[str] = "Aguardando Início"
    labels: List[str] = []
    
    @classmethod
    def from_task(cls, task: Task) -> 'PlannerTask':
        return cls(
            title=task.title,
            description=task.description,
            client=task.client,
            contract=task.contract,
            responsible_email=task.responsible_email,
            requester_email=task.sender_email,
            labels=[cls._set_label(task.client)]
        )

    @staticmethod
    def _set_label(client: str) -> str:
        category = CompanyCategory.get_category(client)
        if not category:
            return "category3"
        return category

    def to_api_format(self) -> dict:
        """Converte para o formato esperado pela API"""
        return self.model_dump(exclude_none=True)