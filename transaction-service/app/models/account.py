from sqlalchemy import Column, DateTime, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base
import datetime


class Account(Base):
    """
    Model representing an account containing a balance.
    """

    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    balance = Column(Numeric(18, 2), nullable=False, default=0)

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )

    __table_args__ = (
        CheckConstraint("balance >= 0", name="check_balance_non_negative"),
    )
