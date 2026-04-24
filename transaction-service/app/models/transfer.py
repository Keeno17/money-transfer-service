from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base
from datetime import datetime, timezone


class TransferStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Transfer(Base):
    """
    Model representing a transfer where money moves between accounts.
    """

    __tablename__ = "transfers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    from_account = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)

    to_account = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)

    amount = Column(Numeric(18, 2), nullable=False)

    status = Column(String(20), nullable=False, default=TransferStatus.PENDING.value)

    idempotency_key = Column(String(255), nullable=False, unique=True)
    request_hash = Column(String(64), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    completed_at = Column(DateTime(timezone=True), nullable=True)

    source_account = relationship("Account", foreign_keys=[from_account])
    destination_account = relationship("Account", foreign_keys=[to_account])

    __table_args__ = (CheckConstraint("amount > 0", name="check_amount_non_negative"),)
