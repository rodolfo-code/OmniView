import logging
from typing import TypedDict
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from app.application.agents.tools.update_tasks_state import generate_random_ints
from app.infrastructure.services.llm.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

def task_extraction_node(state: EmailAnalysisState) -> EmailAnalysisState:
    """
    Gera itens de ação a partir do email.
    """

    logger.info("Iniciando extração de tarefas do e-mail")

    llm_service = LLMFactory.create_llm_service("openai")

    tasks = llm_service.extract_tasks(state.get("raw_email"))

    # tool_response = generate_random_ints.invoke({
    #     "name": "generate_random_ints",
    #     "args": {"min": 0, "max": 9, "size": 10},
    #     "id": "123",  # required
    #     "type": "tool_call",  # required
    # })


    # print("TOOL_RESPONSEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE: ", tool_response)

    print("--- Função externa: PASSO 3: Gerando itens de ação ---")

    return {
        **state,
        "context": "SEND_TASK_CONTEXT",
        "next_step": "START"
    }