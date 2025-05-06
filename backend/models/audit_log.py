from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Enum, Session, select
from uuid import UUID
from ulid import ULID
from backend.database import get_session
from backend.models.user import User

from typing import Optional, Dict, List
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import Json

class ActionType(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"

    DELETE_HARD = "delete_hard"
    ARCHIVE = "archive"
    RESTORE = "restore"

class AuditLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime

    http_method: str
    api_endpoint: str
    resource_type: str
    resource_id: UUID
    request_body: Json

    response_status_code: int
    response_status_message: str
    response_body: Json
    
    action_type: ActionType
    
    source: str = Field(..., description="The origin of the action, e.g., 'web', 'mobile', or 'api'")
    user_id: Optional[int] = Field(default=None, nullable=True)
    team_id: Optional[int] = Field(default=None, nullable=True)
    metadata: Optional[Json] = Field(default=None, nullable=True)
