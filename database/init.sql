CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    balance NUMERIC(18,2) NOT NULL CHECK (balance >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transfers (
    id UUID PRIMARY KEY,
    from_account UUID NOT NULL,
    to_account UUID NOT NULL,
    amount NUMERIC(18,2) NOT NULL CHECK (amount > 0),
    status TEXT NOT NULL CHECK (status IN ('pending', 'completed', 'failed')),
    idempotency_key TEXT NOT NULL UNIQUE,
    request_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    CONSTRAINT fk_from_account FOREIGN KEY (from_account) REFERENCES accounts(id),
    CONSTRAINT fk_to_account FOREIGN KEY (to_account) REFERENCES accounts(id)
);

CREATE TABLE ledger_entries (
    id UUID PRIMARY KEY,
    transfer_id UUID NOT NULL,
    account_id UUID NOT NULL,
    entry_type TEXT NOT NULL CHECK (entry_type IN ('debit', 'credit')),
    amount NUMERIC(18,2) NOT NULL CHECK (amount > 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ledger_transfer FOREIGN KEY (transfer_id) REFERENCES transfers(id),
    CONSTRAINT fk_ledger_account FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    transfer_id UUID NULL,
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_transfer FOREIGN KEY (transfer_id) REFERENCES transfers(id)
);

CREATE INDEX idx_transfers_from_account ON transfers(from_account);
CREATE INDEX idx_transfers_to_account ON transfers(to_account);
CREATE INDEX idx_ledger_entries_transfer_id ON ledger_entries(transfer_id);
CREATE INDEX idx_audit_logs_transfer_id ON audit_logs(transfer_id);