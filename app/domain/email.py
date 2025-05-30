from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

class EmailParticipant(BaseModel):
    name: str
    address: str

class EmailBody(BaseModel):
    content: str
    content_type: str = Field(alias="content_type")

class Email(BaseModel):
    id: str
    subject: str
    sender: EmailParticipant = Field(alias="from")
    recipients: List[EmailParticipant] = Field(alias="to")
    body: EmailBody
    received_date_time: datetime = Field(alias="received_date_time")
    sent_date_time: datetime = Field(alias="sent_date_time")
    is_read: bool = Field(alias="is_read")
    has_attachments: bool = Field(alias="has_attachments")

    class Config:
        populate_by_name = True