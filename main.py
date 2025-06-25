import logging
import os

from fastapi import FastAPI, Request
from dotenv import load_dotenv
from app.presentation.graphMicrosoft.routers import router as graphMicrosoftRouter

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OmniView",
    description="API para o projeto Graph",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(graphMicrosoftRouter, prefix="/graph-microsoft", tags=["Graph Microsoft"])


@app.get("/", summary="Verifica se a API está funcionando")
def read_root():    
    return {
        "message": "API para o projeto Graph",
        "status": "online",
        "version": "0.1.0",
        "docs": "/docs",
    }

    import requests

    url = "https://6d23-89-181-155-219.ngrok-free.app/tasks/batch"
    
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "tasks": [
            {
                "client": "ALLOS",
                "contract": "Sustentação Técnica",
                "title": "Criar banners",
                "status": "Aguardando Início",
                "description": "por favor criar banners",
                "requester": {
                    "name": "Rodolfo Olvieira",
                    "email": "rodolfo.oliveira@allos.com",
                    "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                    },
                "responsible": {
                    "name": "Erick Marinho",
                    "email": "erick.marinho@impar.com",
                    "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                    },
                "createdAt": "20/11/2025"
            },
            {
                "client": "Vale",
                "contract": "Sustentação Técnica",
                "title": "Criar Formulario com SPFX",
                "status": "Aguardando Início",
                "description": "Preciso criar um novo formulario",
                "requester": {
                    "name": "Rodolfo Olvieira",
                    "email": "rodolfo.oliveira@allos.com",
                    "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                    },
                "responsible": {
                    "name": "Erick Marinho",
                    "email": "erick.marinho@impar.com",
                    "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                    },
                "createdAt": "20/11/2025"
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    print("RESPONSE DA APIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII", response.json())
    
    return {
        "message": "verifica se salvou no delta",
        "status": "online",
        "version": "0.1.0",
        "docs": "/docs",
    }