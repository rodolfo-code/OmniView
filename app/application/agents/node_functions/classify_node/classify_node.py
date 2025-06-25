import logging

from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.infrastructure.services.llm.llm_factory import LLMFactory

logger = logging.getLogger(__name__)


def classify_node(state: EmailAnalysisState) -> EmailAnalysisState:
    """
    Classifica o email em uma categoria.
    TASK
    NOT_TASK
    """	

    llm_service = LLMFactory.create_llm_service("openai")
    llm_response = llm_service.classify_email(state["raw_email"])

    return {
        **state,
        "next_step": llm_response
    }
