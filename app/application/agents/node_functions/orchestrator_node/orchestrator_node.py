import logging
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.domain.email import Email
from app.infrastructure.services.llm.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

def orchestrator_node(state: EmailAnalysisState) -> EmailAnalysisState:
    """
    Categoriza o email em uma categoria.
    """

    current_context = state.get("context", "EXTRACT_TASKS_CONTEXT")
   
    logger.info("Iniciando processamento do e-mail")

    if current_context == "EXTRACT_TASKS_CONTEXT":

        llm_service = LLMFactory.create_llm_service("openai")

        classification = llm_service.classify_email(state.get("raw_email"))

    elif current_context == "SEND_TASK_CONTEXT":
        classification = "SEND_TASK"


    logger.info("Classificação do e-mail: %s", classification)

    return {
        **state,
        "next_step": classification
    }