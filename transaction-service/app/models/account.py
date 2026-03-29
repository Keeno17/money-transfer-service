from enum import Enum
from sqlalchemy import Column, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base
import datetime

class Account(Base):
    """
    Model representing an account containing a balance.
    """

    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    balance = Column(Numeric(18, 2), nullable=False)

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )