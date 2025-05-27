import logging 
from app.domain.email import Email

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
        print(f"Serviço de Aplicação: Email '{email_data.subject}' recebido e sendo processado")
        return None