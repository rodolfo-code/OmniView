import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.email import Email, EmailParticipant, EmailBody
from app.application.services.email_service import EmailApplicationService
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)

router = APIRouter()

# Define o diretório para salvar os logs de emails
EMAIL_LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs", "emails")

# Cria o diretório se não existir
os.makedirs(EMAIL_LOGS_DIR, exist_ok=True)

def parse_datetime(date_str: str | None) -> datetime | None:
    """
    Converte uma string de data para datetime, retornando None se a string for vazia ou inválida.
    """
    if not date_str:
        return None
    
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        logger.warning(f"Data inválida recebida: {date_str}")
        return None

def transform_webhook_data(data: dict) -> Email:
    """
    Transforma os dados do webhook para o formato esperado pelo modelo Email.
    """
    try:
        id = data.get("id", "")
        subject = data.get("subject", "")
        sender: EmailParticipant = data.get("from", {})
        recipients: List[EmailParticipant] = data.get("to", [])
        body: EmailBody = data.get("body", {})
        received_date_time = data.get("received_date_time")
        sent_date_time = data.get("sent_date_time")
        is_read = data.get("is_read")
        has_attachments = data.get("has_attachments")
        received_date_time = parse_datetime(data.get("received_date_time"))
        sent_date_time = parse_datetime(data.get("sent_date_time"))

        current_time = datetime.now()
        received_date_time = received_date_time or current_time
        sent_date_time = sent_date_time or current_time

        return Email(
            id=id,
            subject=subject,
            sender=sender,
            recipients=recipients,
            body=body,
            received_date_time=received_date_time,
            sent_date_time=sent_date_time,
            is_read=bool(is_read),
            has_attachments=bool(has_attachments)
        )
    except Exception as e:
        logger.error(f"Erro ao transformar dados do webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar dados do webhook: {str(e)}"
        )

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def processGraphWebhook(email_data: dict, email_service: EmailApplicationService = Depends(EmailApplicationService)):
    """
    Endpoint para processar webhooks do Microsoft Graph contendo dados de email.
    """
    
    try:
        logger.info(f"Dados recebidos do webhook: {json.dumps(email_data, indent=2)}")
        
        email = transform_webhook_data(email_data)
        analysis_result = await email_service.process_incoming_email(email)


        return {
            "message": "E-mail analisado com sucesso",
            "email_id": email.id,
            "analysis": analysis_result,
        }
    
    except Exception as e:
        logger.error(f"Erro ao processar webhook de email: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Ocorreu um erro interno ao processar o webhook do email: {e}"
        )
