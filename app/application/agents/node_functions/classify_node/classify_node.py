import logging

from app.application.agents.state.email_analysis_state import EmailAnalysisState

logger = logging.getLogger(__name__)


def classify_node(state: EmailAnalysisState) -> EmailAnalysisState:
    """
    Classifica o email em uma categoria.
    TASK
    NOT_TASK
    """	


    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", state)


    return {
        **state,
    }
