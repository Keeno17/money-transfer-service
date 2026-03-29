from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account

import uuid


class AccountRepo:

    @staticmethod
    def get_by_id(session: Session, account_id: uuid.UUID) -> Account | None:
        stmt = select(Account).where(Account.id == account_id)

        return session.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_all(session: Session) -> list[Account] | None:
        return session.query(Account).all()

    @staticmethod
    def create(session: Session, account: Account) -> Account:
        session.add(account)

        session.flush()

        session.refresh(account)
        return account

    @staticmethod
    def update(session: Session, account: Account) -> Account:
        session.flush()
        session.refresh(account)
        return account
