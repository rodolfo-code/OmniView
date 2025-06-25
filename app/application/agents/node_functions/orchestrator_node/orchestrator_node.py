import logging
from langchain_core.messages import HumanMessage
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.domain.email import Email
from app.infrastructure.services.llm.llm_factory import LLMFactory



logger = logging.getLogger(__name__)

def orchestrator_node(state: EmailAnalysisState) -> EmailAnalysisState:
    """
    Categoriza o email em uma categoria.
    """
    # messages = state["messages"]

    # if not messages:
    #     initial_human_message = HumanMessage(content=" 'x' = 20, 'y' = 10")
    #     messages = [initial_human_message]

    # llm_service = LLMFactory.create_llm_service("openai")

    # llm_response = llm_service.client_tools(messages)

    

    return {
        **state,
        # "messages": state["messages"] + [llm_response]
    }