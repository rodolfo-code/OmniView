from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/")
def processGraphWebhook():
    return {
        "message": "Webhook processado com sucesso"
    }
