import random
from typing import List, Tuple
from langchain_core.tools import tool

from app.domain.task import Task
from app.application.agents.state.email_analysis_state import EmailAnalysisState

@tool
def update_tasks_state(state: EmailAnalysisState, tasks: List[Task]):
    """Atualiza o estado com a lista de tarefas fornecida.
    
    Args:
        state (EmailAnalysisState): O estado atual da análise de email
        tasks (List[Task]): Lista de tarefas a serem adicionadas ao estado
        
    Returns:
        EmailAnalysisState: O estado atualizado com as novas tarefas
    """
    state["tasks"] = tasks
    return state


@tool(response_format="content_and_artifact")
def generate_random_ints(min: int, max: int, size: int) -> Tuple[str, List[int]]:
    """Generate size random ints in the range [min, max]."""
    array = [random.randint(min, max) for _ in range(size)]
    content = f"Successfully generated array of {size} random ints in [{min}, {max}]."
    return content, array