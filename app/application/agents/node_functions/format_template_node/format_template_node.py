from datetime import datetime
from app.application.agents.state.email_analysis_state import EmailAnalysisState
from langchain_core.messages import HumanMessage, AIMessage

from app.domain.delta_task import DeltaTask
from app.domain.planner_task import PlannerTask
from app.domain.task import Task
from app.infrastructure.services.llm.llm_factory import LLMFactory


def format_template_node(state: EmailAnalysisState) -> EmailAnalysisState:
    """
    Formata o template das tarefas para Planner e Delta
    """

    messages = state["messages"]

    tasks = state.get("tasks", [])

    delta_tasks = [DeltaTask.from_task(task) for task in tasks]

    planner_tasks = [PlannerTask.from_task(task) for task in tasks]


    if not messages:
        initial_human_message = HumanMessage(content=f"Envie as seguintes tarefas para o Delta e para o Planner. Importante: Não altere o formato das tarefas: {delta_tasks} {planner_tasks}")
        messages = [initial_human_message]

    llm_service = LLMFactory.create_llm_service("openai")

    llm_response = llm_service.client_tools(messages)
    
    return {"messages": messages + [llm_response]}
