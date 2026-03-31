from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
import uuid


class CreateAccountRequest(BaseModel):
    balance: Decimal = Field(
        ...,
        ge=0,
        description="The initial balance of the account (must be greater than or equal to 0)",
    )


class GetAccountResponse(BaseModel):
    id: uuid.UUID = Field(..., description="The UUID of the account")
    balance: Decimal = Field(..., description="The current balance of the account")
    created_at: datetime = Field(
        ..., description="The timestamp when the account was created"
    )

    model_config = ConfigDict(from_attributes=True)
