from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class EmailParticipant(BaseModel):
    name: str
    address: str

class EmailBody(BaseModel):
    content: str
    content_type: str = Field(alias="content_type")

class Email(BaseModel):
    id: Optional[str] = None
    subject: Optional[str] = None
    sender: EmailParticipant = Field(alias="from")
    recipients: List[EmailParticipant] = Field(alias="to")
    body: EmailBody
    received_date_time: Optional[datetime] = None
    sent_date_time: Optional[datetime] = None
    is_read: Optional[bool] = None
    has_attachments: Optional[bool] = None

    class Config:
        populate_by_name = True