import logging

from langchain_openai import ChatOpenAI
from app.application.agents.node_functions.orchestrator_node.classify_email_prompt import CLASSIFY_EMAIL_TEMPLATE
from app.application.interfaces.illm_service import ILLMService
from app.domain.email import Email
from app.infrastructure.config.config import settings

logger = logging.getLogger(__name__)

class OpenAIService(ILLMService):
    def __init__(self):
        self.client = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL_NAME,
            temperature=settings.OPENAI_TEMPERATURE
        )

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
        # chain = EXTRACT_TASKS_TEMPLATE | self.client

        # try:
        #     llm_response = chain.invoke({"email": email})
        #     return llm_response.content
        # except Exception as e:
        #     logger.error(f"Erro ao extrair as tarefas do e-mail: {e}")
        #     return None
        pass
