from app.application.interfaces.illm_service import ILLMService
from app.infrastructure.services.llm.openai_service import OpenAIService

class LLMFactory:
    @staticmethod
    def create_llm_service(llm_provider: str) -> ILLMService:

        if llm_provider == "openai":
            return OpenAIService()
        else:
            raise ValueError(f"Provider de LLM não suportado: {llm_provider}")