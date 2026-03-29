from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base
import datetime

class TransferStatus(str, Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    PROCESSING = "processing"

class Transfer(Base):
    """
    Model representing a transfer where money moves between accounts.
    """

    __tablename__ = "transfers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    from_account = Column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False
    )

    to_account = Column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False
    )

    amount = Column(Numeric(18, 2), nullable=False)

    status = Column(SQLEnum(TransferStatus), nullable=False, default=TransferStatus.INCOMPLETE)

    idempotency_key = Column(String(255), nullable=False, unique=True)

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )

    source_account = relationship("Account", foreign_keys=[from_account])
    destination_account = relationship("Account", foreign_keys=[to_account])
