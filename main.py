import logging
import os

from fastapi import FastAPI
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
