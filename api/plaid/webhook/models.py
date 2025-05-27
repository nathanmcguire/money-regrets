from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime


class PlaidWebhookEvent(BaseModel):
    webhook_type: str
    webhook_code: str
    item_id: Optional[str] = None
    error: Optional[str] = None
    # Add more fields as needed for specific webhook types
    # Use extra fields to allow arbitrary keys

    class Config:
        extra = "allow"


class PlaidWebhook(SQLModel, table=True):
    __tablename__ = "plaid_webhooks"
    id: int = Field(default=None, primary_key=True)
    body: str
    headers: str
    received_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = Field(default=False)
    processing_error: str = Field(default=None, nullable=True)
