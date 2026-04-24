from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.api.deps import get_db_session

from app.schemas.transfer_schema import (
    CreateTransferRequest,
    GetTransferResponse,
)

from app.services.transfer_service import TransferService

from app.core.security import verify_service_api_key
from app.core.exceptions import (
    ValidationError,
    TransferNotFoundError,
    AccountNotFoundError,
    InsufficientFundsError,
    IdempotencyKeyConflictError,
)

router = APIRouter(
    prefix="/transfers",
    dependencies=[Depends(verify_service_api_key)],
)


@router.post("/", response_model=GetTransferResponse)
async def create_transfer(
    transfer_request: CreateTransferRequest,
    session: Session = Depends(get_db_session),
) -> GetTransferResponse:
    try:
        new_transfer = TransferService.create_transfer(
            session=session,
            from_account=transfer_request.from_account,
            to_account=transfer_request.to_account,
            amount=transfer_request.amount,
            idempotency_key=transfer_request.idempotency_key,
        )
        return GetTransferResponse.model_validate(new_transfer)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TransferNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IdempotencyKeyConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InsufficientFundsError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/{transfer_id}", response_model=GetTransferResponse)
async def get_transfer_by_id(
    transfer_id: uuid.UUID, 
    session: Session = Depends(get_db_session),
) -> GetTransferResponse:
    try:
        transfer = TransferService.get_transfer_by_id(session, transfer_id)
        return GetTransferResponse.model_validate(transfer)
    except TransferNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[GetTransferResponse])
async def list_transfers(
    session: Session = Depends(get_db_session),
) -> list[GetTransferResponse]:
    transfers = TransferService.get_all_transfers(session)
    return [GetTransferResponse.model_validate(t) for t in transfers]
