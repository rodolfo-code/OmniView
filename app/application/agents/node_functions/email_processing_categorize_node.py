from typing import TypedDict
from app.domain.email import Email

class EmailInputState(TypedDict):
    email: Email

class CategoryOutputState(TypedDict):
    category: str

def categorize_node(state: EmailInputState) -> CategoryOutputState:
    """
    Categoriza o email em uma categoria.
    """
    print("--- Função externa: PASSO 2: Categorizando o e-mail ---")
    return {"category": "Categoria do e-mail"}