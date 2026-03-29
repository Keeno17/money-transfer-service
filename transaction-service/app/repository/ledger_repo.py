from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ledger import LedgerEntry

import uuid


class LedgerRepo:

    @staticmethod
    def get_by_id(session: Session, ledger_id: uuid.UUID) -> LedgerEntry | None:
        stmt = select(LedgerEntry).where(LedgerEntry.id == ledger_id)

        return session.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_all(session: Session) -> list[LedgerEntry] | None:
        return session.query(LedgerEntry).all()

    @staticmethod
    def create(session: Session, ledger: LedgerEntry) -> LedgerEntry:
        session.add(ledger)

        session.flush()

        session.refresh(ledger)
        return ledger

    @staticmethod
    def update(session: Session, ledger: LedgerEntry) -> LedgerEntry:
        session.flush()
        session.refresh(ledger)
        return ledger
