class TransferServiceError(Exception):
    """Base exception for transfer service errors."""


class ValidationError(TransferServiceError):
    """Raised when there is a validation error in the input data."""


class TransferNotFoundError(TransferServiceError):
    """Raised when a transfer with the specified ID is not found."""


class AccountNotFoundError(TransferServiceError):
    """Raised when an account with the specified ID is not found."""


class InsufficientFundsError(TransferServiceError):
    """Raised when the source account does not have enough balance for the transfer."""


class IdempotencyKeyConflictError(TransferServiceError):
    """Raised when there is a conflict with the idempotency key."""
