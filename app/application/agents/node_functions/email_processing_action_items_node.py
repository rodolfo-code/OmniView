from typing import TypedDict
from app.domain.email import Email

class EmailInputState(TypedDict):
    email: Email

class ActionItemsOutputState(TypedDict):
    action_items: list[str]

def action_items_node(state: EmailInputState) -> ActionItemsOutputState:
    """
    Gera itens de ação a partir do email.
    """
    print("--- Função externa: PASSO 3: Gerando itens de ação ---")
    return {"action_items": ["Item de ação 1", "Item de ação 2"]}