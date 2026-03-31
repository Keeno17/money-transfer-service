from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transfer import Transfer

import uuid


class TransferRepo:

    @staticmethod
    def get_by_id(session: Session, transfer_id: uuid.UUID) -> Transfer | None:
        stmt = select(Transfer).where(Transfer.id == transfer_id)

        return session.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_all(session: Session) -> list[Transfer]:
        return session.query(Transfer).all()

    @staticmethod
    def create(session: Session, transfer: Transfer) -> Transfer:
        session.add(transfer)

        session.flush()

        session.refresh(transfer)
        return transfer

    @staticmethod
    def update(session: Session, transfer: Transfer) -> Transfer:
        session.flush()
        session.refresh(transfer)
        return transfer

    @staticmethod
    def get_by_idempotency_key(
        session: Session, idempotency_key: str
    ) -> Transfer | None:
        stmt = select(Transfer).where(Transfer.idempotency_key == idempotency_key)
        return session.execute(stmt).scalar_one_or_none()
