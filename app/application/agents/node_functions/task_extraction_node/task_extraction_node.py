import logging
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.domain.task import Task
from app.infrastructure.services.llm.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

def task_extraction_node(state: EmailAnalysisState) -> EmailAnalysisState:
    """
    Gera itens de ação a partir do email.
    """

    logger.info("Iniciando extração de tarefas do e-mail")

    llm_service = LLMFactory.create_llm_service("openai")

    llm_response: list[Task] = llm_service.extract_tasks(state.get("raw_email"))

    return {
        **state,
        "tasks": llm_response,
    }