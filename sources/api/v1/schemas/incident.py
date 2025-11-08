from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class IncidentStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class IncidentSourceStr(str, Enum):
    operator = "operator"
    monitoring = "monitoring"


class IncidentCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=225)
    status: IncidentStatus
    source: IncidentSourceStr


class IncidentUpdate(BaseModel):
    description: str | None = None
    status: IncidentStatus | None = None
    source: IncidentSourceStr | None = None


class IncidentResponse(BaseModel):
    id: int
    description: str
    status: IncidentStatus
    source: IncidentSourceStr
    created_at: datetime
