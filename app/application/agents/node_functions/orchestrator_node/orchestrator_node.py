import logging
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.domain.email import Email
from app.infrastructure.services.llm.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

def orchestrator_node(state: EmailAnalysisState) -> EmailAnalysisState:
    """
    Categoriza o email em uma categoria.
    """

    logger.info("Iniciando processamento do e-mail")
    logger.info("E-mail: %s", state.get("raw_email"))

    llm_service = LLMFactory.create_llm_service("openai")

    classification = llm_service.classify_email(state.get("raw_email"))

    logger.info("Classificação do e-mail: %s", classification)

    return {
        **state,
        "next_step": classification
    }