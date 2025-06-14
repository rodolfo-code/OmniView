from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str
    company: str
    sender: str
    in_charge: str