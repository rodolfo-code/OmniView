from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="OmniView",
    description="OmniView is a web application that allows you to view your home from anywhere.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}