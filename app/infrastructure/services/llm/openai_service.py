import json
import logging
from typing import Callable, Sequence

from langchain_openai import ChatOpenAI
from app.application.agents.node_functions.orchestrator_node.classify_email_prompt import CALCULATOR_PROMPT_TEMPLATE, CLASSIFY_EMAIL_TEMPLATE
from app.application.agents.node_functions.task_extraction_node.tasks_extract_prompt import TASKS_EXTRACT_TEMPLATE
from app.application.agents.tools.calculator_tool import calculator_tool, divide_tool
from app.application.interfaces.illm_service import ILLMService
from app.domain.email import Email
from app.infrastructure.config.config import settings
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from langgraph.prebuilt import ToolNode

logger = logging.getLogger(__name__)

class OpenAIService(ILLMService):
    def __init__(self):
        self.client = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL_NAME,
            temperature=settings.OPENAI_TEMPERATURE
        )

        self.client_with_tools = self.client.bind_tools([calculator_tool, divide_tool])

        # self.client_with_tools = ToolNode([calculator_tool])

    def client_tools(self, messages: Sequence[BaseMessage]):

        chains = CALCULATOR_PROMPT_TEMPLATE | self.client_with_tools

        llm_response = chains.invoke({"messages": messages})

        print("LLM RESPONSE", llm_response)

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
        from langchain_core.prompts import ChatPromptTemplate
        from langgraph.prebuilt import ToolNode
        from langchain_core.messages import AIMessage

        chain = TASKS_EXTRACT_TEMPLATE | self.client

        try:
            
            
            llm_response = chain.invoke({"email_content": email})



            response_data = json.loads(llm_response.content)

            # tool_node = ToolNode([generate_random_ints])

            # update_tasks_state_tool = [
            #     {
            #         "name": "update_tasks_state",
            #         "args": {"state": state, "tasks": response_data },
            #         "id": "123",
            #         "type": "tool_call"
            #     }
            # ]

            
            tool_calls = [
                {
                    "name": "generate_random_ints",
                    "args": {"min": 0, "max": 9, "size": 10},
                    "id": "123",
                    "type": "tool_call"
                }
            ]
        
            
            # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", tool_node.invoke(update_tasks_state_tool))
            # chain = GENERATE_RANDOM_INTS_TEMPLATE | tool_node | self.client

            # chain.invoke({"email_content": email})

        

        
            
            return response_data
        except Exception as e:
            logger.error(f"Erro ao extrair as tarefas do e-mail: {e}")
            return None
