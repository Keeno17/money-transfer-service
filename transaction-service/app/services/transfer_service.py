from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session
import uuid
import hashlib

from app.models.transfer import Transfer, TransferStatus
from app.models.ledger import LedgerEntry, EntryType
from app.models.account import Account
from app.repository.transfer_repo import TransferRepo
from app.repository.account_repo import AccountRepo
from app.repository.ledger_repo import LedgerRepo


class TransferService:

    @staticmethod
    def get_transfer_by_id(session: Session, transfer_id: uuid.UUID) -> Transfer | None:
        if not transfer_id:
            raise ValueError("Transfer ID must be provided")
        return TransferRepo.get_by_id(session, transfer_id)

    @staticmethod
    def get_all_transfers(session: Session) -> list[Transfer]:
        return TransferRepo.get_all(session)

    @staticmethod
    def create_transfer(
        session: Session,
        from_account: uuid.UUID,
        to_account: uuid.UUID,
        amount: Decimal,
        idempotency_key: str,
    ) -> Transfer:

        if not from_account or not to_account:
            raise ValueError("Both source and destination account must be provided")

        if from_account == to_account:
            raise ValueError("Source and destination account cannot be the same")

        if not amount or amount <= 0:
            raise ValueError("Amount must be greater than 0")

        if not idempotency_key:
            raise ValueError("Idempotency key must be provided")

        existing_transfer = TransferRepo.get_by_idempotency_key(
            session, idempotency_key
        )

        amount = amount.quantize(Decimal("0.01"))

        request_fingerprint = hashlib.sha256(
            from_account.bytes + to_account.bytes + str(amount).encode()
        ).hexdigest()

        if existing_transfer:
            if request_fingerprint != existing_transfer.request_hash:
                raise ValueError(
                    "A transfer with the same idempotency key already exists with different details"
                )
            return existing_transfer

        src_account, dest_account = AccountRepo.get_two_accounts_for_update(
            session, from_account, to_account
        )

        if not src_account or not dest_account:
            raise ValueError("Both the source and destination account must exist")

        if src_account.balance < amount:
            raise ValueError("Insufficient funds in the source account")

        try:
            new_transfer = Transfer(
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                status=TransferStatus.PENDING,
                idempotency_key=idempotency_key,
                request_hash=request_fingerprint,
            )

            new_transfer = TransferRepo.create(session, new_transfer)

            TransferService.debit_account(src_account, amount)
            TransferService.credit_account(dest_account, amount)

            TransferService.create_ledger_entry(session, new_transfer, from_account)
            TransferService.create_ledger_entry(session, new_transfer, to_account)

            new_transfer.status = TransferStatus.COMPLETED
            new_transfer.completed_at = datetime.now(timezone.utc)

            session.commit()
            return new_transfer
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def create_ledger_entry(
        session: Session,
        transfer: Transfer,
        account_id: uuid.UUID,
    ) -> LedgerEntry:

        if not transfer:
            raise ValueError("Transfer must be provided")
        if not account_id:
            raise ValueError("Account ID must be provided")

        amount = transfer.amount

        if transfer.from_account == account_id:
            entry_type = EntryType.DEBIT
        elif transfer.to_account == account_id:
            entry_type = EntryType.CREDIT
        else:
            raise ValueError(
                "Account ID does not match either the source or destination account of the transfer"
            )

        new_ledger_entry = LedgerEntry(
            account_id=account_id,
            amount=amount,
            entry_type=entry_type,
            transfer_id=transfer.id,
        )

        new_ledger_entry = LedgerRepo.create(session, new_ledger_entry)

        return new_ledger_entry

    @staticmethod
    def debit_account(account: Account, amount: Decimal) -> None:
        if not account:
            raise ValueError("Account must be provided")
        account.balance -= amount

    @staticmethod
    def credit_account(account: Account, amount: Decimal) -> None:
        if not account:
            raise ValueError("Account must be provided")
        account.balance += amount
