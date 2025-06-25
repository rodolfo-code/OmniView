from typing import List

import requests
from app.domain.planner_task import PlannerTask
from langchain_core.tools import tool


@tool
def create_task_in_planner(tasks: List[PlannerTask]) -> dict:
    """
    Cria uma tarefa no Planner enviando uma lista de tasks.

    Args:
        tasks: Lista de tarefas a serem criadas

    Returns:
        Resposta da API
    """


    try:

        url = "https://outlook-webhook.livelygrass-5e1cbc66.brazilsouth.azurecontainerapps.io/api/planner/task"

        headers = {
            "Content-Type": "application/json"
        }

        api_tasks = [task.to_api_format() for task in tasks]


        data = {
            "tasks": api_tasks
        }

        response = requests.post(url, json=api_tasks[0], headers=headers)

        return response.json()
    
    except Exception as e:
        print("ERRO AO CRIAR TAREFA NO PLANNER", e)
        return {"error": str(e)}