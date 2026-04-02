from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base
from datetime import datetime, timezone


class EventType(str, Enum):
    VALIDATION_FAILED = "validation failed"
    TRANSFER_REQUESTED = "transfer requested"
    TRANSFER_COMPLETED = "transfer completed"
    TRANSFER_FAILED = "transfer failed"
    IDEMPOTENCY_REPLAY = "idempotency replay"


class AuditLog(Base):
    """
    Model representing a audit log.
    """

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    event_type = Column(SQLEnum(EventType))

    transfer_id = Column(UUID(as_uuid=True), ForeignKey("transfers.id"), nullable=True)

    message = Column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    transfer = relationship("Transfer")
