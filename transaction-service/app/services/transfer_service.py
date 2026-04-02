from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session
import uuid
import hashlib
import logging

from app.models.transfer import Transfer, TransferStatus
from app.models.ledger import LedgerEntry, EntryType
from app.models.account import Account
from app.models.audit import AuditLog, EventType
from app.repository.transfer_repo import TransferRepo
from app.repository.account_repo import AccountRepo
from app.repository.audit_repo import AuditRepo
from app.repository.ledger_repo import LedgerRepo

from app.core.exceptions import (
    ValidationError,
    TransferNotFoundError,
    AccountNotFoundError,
    InsufficientFundsError,
    IdempotencyKeyConflictError,
)

logger = logging.getLogger(__name__)


class TransferService:

    @staticmethod
    def debit_account(account: Account, amount: Decimal) -> None:
        if not account:
            logger.warning("Debit failed: account was not provided")
            raise ValidationError("Account must be provided")
        if amount <= 0:
            logger.warning("Debit failed: amount must be greater than 0")
            raise ValidationError("Amount must be greater than 0")
        account.balance -= amount

    @staticmethod
    def credit_account(account: Account, amount: Decimal) -> None:
        if not account:
            logger.warning("Credit failed: account was not provided")
            raise ValidationError("Account must be provided")
        if amount <= 0:
            logger.warning("Credit failed: amount must be greater than 0")
            raise ValidationError("Amount must be greater than 0")
        account.balance += amount

    @staticmethod
    def get_transfer_by_id(session: Session, transfer_id: uuid.UUID) -> Transfer | None:
        if not transfer_id:
            logger.warning("Transfer lookup failed: transfer_id was not provided")
            raise ValidationError("Transfer ID must be provided")
        try:
            return TransferRepo.get_by_id(session, transfer_id)
        except Exception:
            raise TransferNotFoundError(f"Transfer with ID {transfer_id} not found")

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
            logger.warning("Missing source or destination account in transfer service")
            raise ValidationError(
                "Both source and destination account must be provided"
            )

        if from_account == to_account:
            logger.warning(
                "Source and destination account are the same in transfer service"
            )
            raise ValidationError("Source and destination account cannot be the same")

        if not amount or amount <= 0:
            logger.warning("Invalid transfer amount provided in transfer service")
            raise ValidationError("Amount must be greater than 0")

        if not idempotency_key:
            logger.warning("No idempotency key provided in transfer service")
            raise ValidationError("Idempotency key must be provided")

        existing_transfer = TransferRepo.get_by_idempotency_key(
            session, idempotency_key
        )

        amount = amount.quantize(Decimal("0.01"))

        request_fingerprint = hashlib.sha256(
            from_account.bytes + to_account.bytes + str(amount).encode()
        ).hexdigest()

        if existing_transfer:
            if request_fingerprint != existing_transfer.request_hash:
                logger.warning(
                    "Duplicate idempotency key with different request details"
                )
                TransferService._log_event(
                    session,
                    existing_transfer.id,
                    EventType.VALIDATION_FAILED,
                    "Duplicate idempotency key with different request details",
                )
                session.commit()
                raise IdempotencyKeyConflictError(
                    "A transfer with the same idempotency key already exists with different details"
                )
            TransferService._log_event(
                session,
                existing_transfer.id,
                EventType.IDEMPOTENCY_REPLAY,
                "Duplicate idempotency key returned existing transfer",
            )
            session.commit()
            return existing_transfer

        src_account, dest_account = AccountRepo.get_two_accounts_for_update(
            session, from_account, to_account
        )

        if not src_account or not dest_account:
            logger.warning("One or both accounts do not exist")
            raise AccountNotFoundError(
                "Both the source and destination account must exist"
            )

        if src_account.balance < amount:
            logger.warning("Insufficient funds in the source account")
            raise InsufficientFundsError("Insufficient funds in the source account")

        new_transfer = None

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

            logger.info("Transfer %s completed successfully", new_transfer.id)
            TransferService._log_event(
                session,
                new_transfer.id,
                EventType.TRANSFER_COMPLETED,
                "Transfer processing completed and committed to the database",
            )
            session.commit()
            session.refresh(new_transfer)

            return new_transfer
        except Exception:
            session.rollback()
            logger.exception(
                "Transfer processing failed and database rollback occurred"
            )
            try:
                TransferService._log_event(
                    session,
                    new_transfer.id if new_transfer else None,
                    EventType.TRANSFER_FAILED,
                    "An error occurred during transfer processing and database rollback occurred",
                )
                session.commit()
            except Exception:
                session.rollback()
                logger.exception("Failed to log transfer failure event after rollback")
            raise

    @staticmethod
    def create_ledger_entry(
        session: Session,
        transfer: Transfer,
        account_id: uuid.UUID,
    ) -> LedgerEntry:

        if not transfer:
            logger.warning("Ledger entry failed: transfer was not provided")
            raise ValidationError("Transfer must be provided")
        if not account_id:
            logger.warning("Ledger entry failed: account_id was not provided")
            raise ValidationError("Account ID must be provided")

        amount = transfer.amount

        if transfer.from_account == account_id:
            entry_type = EntryType.DEBIT
        elif transfer.to_account == account_id:
            entry_type = EntryType.CREDIT
        else:
            logger.warning(
                "Ledger entry failed: Account ID does not match either the source or destination account of the transfer"
            )
            raise AccountNotFoundError(
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
    def _log_event(
        session: Session,
        transfer_id: uuid.UUID | None,
        event_type: EventType,
        message: str,
    ) -> None:

        if not event_type:
            logger.warning("Audit log failed: No event type provided")
            raise ValidationError("Event type must be provided")
        if not message:
            logger.warning("Audit log failed: No message provided")
            raise ValidationError("Message must be provided")

        new_audit_log = AuditLog(
            transfer_id=transfer_id,
            event_type=event_type,
            message=message,
        )

        AuditRepo.create(session, new_audit_log)
