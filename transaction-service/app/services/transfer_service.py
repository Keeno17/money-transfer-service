from decimal import Decimal
from sqlalchemy.orm import Session
import uuid

from app.models.transfer import Transfer, TransferStatus
from app.repository.transfer_repo import TransferRepo

class TransferService:

    @staticmethod
    def get_transfer_by_id(session: Session, transfer_id: uuid.UUID) -> Transfer | None:
        if not transfer_id:
            raise ValueError("Transfer ID must be provided")
        return TransferRepo.get_by_id(session, transfer_id)

    @staticmethod
    def get_all_transfers(session: Session) -> list[Transfer] | None:
        return TransferRepo.get_all(session)


    @staticmethod
    def create_transfer(
        session: Session, 
        from_account: uuid.UUID, 
        to_account: uuid.UUID, 
        amount: Decimal, 
        idempotency_key: str
        ) -> Transfer:

        if not from_account or not to_account:
            raise ValueError("Both from_account and to_account must be provided")

        if not amount or amount <= 0:
            raise ValueError("Amount must be greater than 0")

        if not idempotency_key:
            raise ValueError("Idempotency key must be provided")

        new_transfer = Transfer(
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            idempotency_key=idempotency_key,
            )

        new_transfer = TransferRepo.create(session, new_transfer)

        session.commit()

        return new_transfer



