from pydantic import BaseModel
from typing import List, Optional

class Person(BaseModel):
    name: str
    email: str
    avatar: Optional[str] = ""
