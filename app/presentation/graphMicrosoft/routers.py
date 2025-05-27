import logging
from fastapi import APIRouter, HTTPException, status
from app.domain.email import Email
from app.application.services.email_service import EmailApplicationService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_ACCEPTED)
async def processGraphWebhook(email_data: Email):
    """
    Endpoint para processar webhooks do Microsoft Graph contendo dados de email.
    """
    email_service = EmailApplicationService()
    try:
        logger.info(f"Recebendo webhook do Microsoft Graph para o email: {email_data.id}")
        await email_service.process_incoming_email(email_data)
        return {
            "message": "Webhook processado com sucesso",
            "email_id": email_data.id
        }
    except Exception as e:
        logger.error(f"Erro ao processar webhook de email: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Ocorreu um erro interno ao processar o webhook do email: {e}"
        )
