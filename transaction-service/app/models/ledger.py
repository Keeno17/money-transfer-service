from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base
import datetime

class EntryType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"

class LedgerEntry(Base):
    """
    Model representing a ledger.
    """

    __tablename__ = "ledger_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    account_id = Column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False
    )

    amount = Column(Numeric(18, 2), nullable=False)

    entry_type = Column(SQLEnum(EntryType))

    transfer_id = Column(
        UUID(as_uuid=True), ForeignKey("transfers.id")
    )

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )

    account = relationship("Account")
    transfer = relationship("Transfer")