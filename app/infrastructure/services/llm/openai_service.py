import json
import logging
from typing import Callable, Sequence
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from app.application.agents.node_functions.orchestrator_node.classify_email_prompt import CLASSIFY_EMAIL_TEMPLATE
from app.application.agents.node_functions.task_extraction_node.tasks_extract_prompt import TASKS_EXTRACT_TEMPLATE
from app.application.agents.node_functions.tool_node.insert_tasks_prompt import INSERT_TASKS_TEMPLATE
from app.application.agents.tools.delta_api_tool import create_task_in_delta
from app.application.agents.tools.planner_api_tool import create_task_in_planner
from app.application.interfaces.illm_service import ILLMService
from app.domain.email import Email
from app.domain.task import Task
from app.infrastructure.config.config import settings



logger = logging.getLogger(__name__)

class OpenAIService(ILLMService):
    def __init__(self):
        self.client = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL_NAME,
            temperature=settings.OPENAI_TEMPERATURE
        )

        self.client_with_tools = self.client.bind_tools([create_task_in_delta, create_task_in_planner])

    def client_tools(self, messages: Sequence[BaseMessage]):

        chain = INSERT_TASKS_TEMPLATE | self.client_with_tools

        llm_response = chain.invoke({"messages": messages})

        return llm_response


    def classify_email(self, email: Email) -> str:
        chain = CLASSIFY_EMAIL_TEMPLATE | self.client

        try:
            llm_response = chain.invoke({"email": email})

            logger.info(f"Resposta do LLM: {llm_response.content}")

            return llm_response.content
        except Exception as e:
            logger.error(f"Erro ao classificar o e-mail: {e}")
            return None

    def extract_tasks(self, email: Email) -> list[str]:
        chain = TASKS_EXTRACT_TEMPLATE | self.client

        try:

            llm_response = chain.invoke({"email_content": email})

            response_data = json.loads(llm_response.content)

            tasks = [Task(**task_data) for task_data in response_data]

            return tasks
        except Exception as e:
            logger.error(f"Erro ao extrair as tarefas do e-mail: {e}")
            return None
