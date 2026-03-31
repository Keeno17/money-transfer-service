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
    def get_two_accounts_for_update(
        session: Session, id1: uuid.UUID, id2: uuid.UUID
    ) -> tuple[Account | None, Account | None]:

        stmt = (
            select(Account)
            .where(Account.id.in_(sorted([id1, id2])))
            .order_by(Account.id)
            .with_for_update()
        )

        results = session.execute(stmt).scalars().all()

        account_map = {account.id: account for account in results}

        return (
            account_map.get(id1),
            account_map.get(id2),
        )

    @staticmethod
    def get_all(session: Session) -> list[Account]:
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
