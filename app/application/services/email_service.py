import logging 
from app.domain.email import Email
from app.application.agents.email_analyzer_agent_builder import EmailAgentBuilder

logger = logging.getLogger(__name__)

class EmailApplicationService:
    async def process_incoming_email(self, email_data: Email) -> None:
        """
        Processa um email recebido.

        Args:
            email_data: Email recebido.

        Returns:
            None
        """
        logger.info(f"Processing email recebido com ID: {email_data.id} e Assunto: {email_data.subject}")

        builder = EmailAgentBuilder()
        email_analyzer_app = builder.get_app()
        
        initial_state = {"email": email_data}

        final_state = email_analyzer_app.invoke(initial_state)

        result = {
            "summary": final_state.get("summary"),
            "category": final_state.get("category"),
            "action_items": final_state.get("action_items")
        }
        
        logger.info(f"Análise do e-mail concluída: {result}")
        print(f"Resultado da análise: {result}")
        return result