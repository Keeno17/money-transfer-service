from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, CheckConstraint, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base
from datetime import datetime, timezone


class EntryType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class LedgerEntry(Base):
    """
    Model representing a ledger.
    """

    __tablename__ = "ledger_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)

    amount = Column(Numeric(18, 2), nullable=False)

    entry_type = Column(String(20), nullable=False)

    transfer_id = Column(UUID(as_uuid=True), ForeignKey("transfers.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    account = relationship("Account")
    transfer = relationship("Transfer")

    __table_args__ = (CheckConstraint("amount > 0", name="check_amount_non_negative"),)
