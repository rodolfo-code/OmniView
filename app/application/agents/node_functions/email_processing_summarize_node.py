from typing import TypedDict
from app.domain.email import Email

class EmailInputState(TypedDict):
    email: Email

class SummaryOutputState(TypedDict):
    summary: str

def summarize_node(state: EmailInputState) -> SummaryOutputState:
    """
    Gera um resumo do email.
    """
    print("--- Função externa: PASSO 1: Resumindo o e-mail ---")

    return {"summary": "Resumo do e-mail"}