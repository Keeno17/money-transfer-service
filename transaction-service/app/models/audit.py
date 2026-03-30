from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base
import datetime

class EventType(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFORMATION = "information"
    SUCCESS = "success"
    FAILURE = "failure"

class AuditLog(Base):
    """
    Model representing a audit log.
    """

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    event_type = Column(SQLEnum(EventType))

    transfer_id = Column(
        UUID(as_uuid=True), ForeignKey("transfers.id")
    )

    message = Column(String(255))

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )

    transfer = relationship("Transfer")