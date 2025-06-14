from typing import TypedDict
from app.domain.email import Email
from app.domain.task import Task

class EmailAnalysisState(TypedDict):
    tasks: list[Task]
    raw_email: Email

    next_step: str
