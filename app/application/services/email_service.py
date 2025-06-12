import logging 
from app.domain.email import Email
from app.application.agents.agent_builder.email_analyzer_agent_builder import EmailAgentBuilder

logger = logging.getLogger(__name__)

class EmailApplicationService:
    def __init__(self):
        self.email_agent_builder = EmailAgentBuilder()
        self.email_agent = self.email_agent_builder.build_agent()

    async def process_incoming_email(self, email_data: Email) -> None:
        """
        Processa um email recebido.
        """
        # logger.info(f"Processing email recebido com ID: {email_data.id} e Assunto: {email_data.subject}")

        initial_state = {
            "raw_email": email_data,
            "tasks": [],
            "next_step": None
        }

        final_state = self.email_agent.invoke(initial_state)

        result = {
            **initial_state,
            "raw_email": final_state.get("raw_email"),
            "tasks": final_state.get("tasks", [])
        }
        
        logger.info(f"Análise do e-mail concluída: {result}")
        print(f"Resultado da análise: {result}")
        return result