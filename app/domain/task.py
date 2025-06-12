from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str
    company: str
    in_charge: str