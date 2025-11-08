import enum
from datetime import datetime

from sqlalchemy import DateTime, String, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from sources.database import Base, ObjectManager


class IncidentStatus(enum.Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class IncidentSource(enum.Enum):
    operator = "operator"
    monitoring = "monitoring"


class Incident(Base, ObjectManager):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[IncidentStatus] = mapped_column(Enum(IncidentStatus), nullable=False)
    source: Mapped[IncidentSource] = mapped_column(Enum(IncidentSource), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
