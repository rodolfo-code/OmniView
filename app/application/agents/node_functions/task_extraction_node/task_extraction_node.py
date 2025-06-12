import logging
from typing import TypedDict
from app.application.agents.state.email_analysis_state import EmailAnalysisState

logger = logging.getLogger(__name__)

def task_extraction_node(state: EmailAnalysisState) -> EmailAnalysisState:
    """
    Gera itens de ação a partir do email.
    """

    logger.info("Iniciando extração de tarefas do e-mail")
    
    print("--- Função externa: PASSO 3: Gerando itens de ação ---")
    return {
        **state,
        "next_step": "END"
    }