from typing import TypedDict
from app.domain.email import Email

class EmailAnalysisState(TypedDict):
    """
    Representa o estado do agente de análise de email.
    """
    email: Email
    summary: str | None = None
    category: str | None = None
    action_items: list[str] | None = None
