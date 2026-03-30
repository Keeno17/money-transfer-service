from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.models.transfer import TransferStatus
import uuid


class CreateTransferRequest(BaseModel):
    from_account: uuid.UUID = Field(..., description="The UUID of the account to transfer from")
    to_account: uuid.UUID = Field(..., description="The UUID of the account to transfer to")
    amount: Decimal = Field(..., gt=0, description="The amount to transfer (must be greater than 0)")
    idempotency_key: str = Field(..., description="A unique key to ensure idempotency of the transfer request")


class GetTransferResponse(BaseModel):
    id: uuid.UUID = Field(..., description="The UUID of the transfer")
    from_account: uuid.UUID = Field(..., description="The UUID of the account to transfer from")
    to_account: uuid.UUID = Field(..., description="The UUID of the account to transfer to")
    amount: Decimal = Field(..., description="The amount transferred")
    status: TransferStatus = Field(..., description="The status of the transfer")
    idempotency_key: str = Field(..., description="The idempotency key used for the transfer request")
    created_at: datetime = Field(..., description="The timestamp when the transfer was created")

    model_config = ConfigDict(from_attributes=True)