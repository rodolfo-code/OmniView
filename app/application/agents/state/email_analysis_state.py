from typing import Annotated, List, Optional, TypedDict
from app.domain.email import Email
from app.domain.task import Task
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class EmailAnalysisState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    tasks: list[Task]
    raw_email: Email

    context: str
    next_step: str
    classification: str

    contract_id: Optional[str]
    contracts_for_choice: Optional[List[dict]]


    multiplication_result: int
