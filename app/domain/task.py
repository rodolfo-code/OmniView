from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str
    client: str
    contract: str
    sender: str
    sender_email: str
    responsible: str
    responsible_email: str
