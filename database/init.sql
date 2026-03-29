CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    balance NUMERIC NOT NULL CHECK (balance >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transfers (
    id UUID PRIMARY KEY,
    from_account UUID NOT NULL,
    to_account UUID NOT NULL,
    amount NUMERIC NOT NULL CHECK (amount > 0),
    status TEXT NOT NULL,
    idempotency_key TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ledger_entries (
    id UUID PRIMARY KEY,
    account_id UUID NOT NULL,
    amount NUMERIC NOT NULL,
    entry_type TEXT CHECK (entry_type IN ('debit', 'credit')),
    transfer_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    event_type TEXT,
    transfer_id UUID,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);