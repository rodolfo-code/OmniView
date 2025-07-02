from typing import List
import json
import os
from datetime import datetime

import requests
from app.domain.delta_task import DeltaTask
from app.domain.task import Task

from langchain_core.tools import tool


def save_tasks_to_json(tasks: List[Task], directory: str = "data") -> str:
    """
    Salva as tasks em um arquivo JSON dentro do diretório especificado.
    
    Args:
        tasks: Lista de tarefas a serem salvas
        directory: Diretório onde o arquivo será salvo (padrão: "data")
    
    Returns:
        Caminho do arquivo salvo
    """
    # Cria o diretório se não existir
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Gera nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tasks_{timestamp}.json"
    filepath = os.path.join(directory, filename)
    
    # Converte tasks para formato serializável
    tasks_data = []
    for task in tasks:
        tasks_data.append(task.model_dump())
    
    # Salva no arquivo JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=2)
    
    print(f"Tasks salvas em: {filepath}")
    return filepath

@tool
def create_task_in_delta(tasks: List[DeltaTask]) -> dict:
    """
    Cria tasks no Delta enviando uma lista de tasks.

    Args:
        tasks: Lista de tarefas a serem criadas

    Returns:
        Resposta da API
    """

    try:
        # Salva as tasks em arquivo JSON
        save_tasks_to_json(tasks)
    

        url = "https://01f7-179-127-37-53.ngrok-free.app/tasks/batch"
        
        headers = {
            "Content-Type": "application/json"
        }

        api_tasks = [task.to_api_format() for task in tasks]

        data = {
            "tasks": api_tasks
        }

        response = requests.post(url, json=data, headers=headers)
    
        return response.json()
        # return {"message": "Tarefas criadas com sucesso"}

    except Exception as e:
        print("ERRO AO CRIAR TAREFA NO DELTA", e)
        return {"error": str(e)}