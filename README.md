# Money Transfer Service

A backend money transfer system built with Node.js, FastAPI, and PostgreSQL, designed to support idempotent transfers, transactional consistency, audit logging, and double-entry ledger records.

## Overview

This project simulates a production-style money transfer workflow where funds move safely between accounts.

## Key features and design decisions

- **Idempotent transfers** using an idempotency key to prevent accidental duplicate processing
- **Transactional consistency** using PostgreSQL transactions
- **Row-level locking** to protect account balance updates during concurrent requests
- **Double-entry ledger records** for each successful transfer
- **Audit logging** for transfer lifecycle events
- **Service-to-service API key protection** between the Node gateway and Python service

## Structure
```text
money-transfer-service/
├── gateway/                  # Node.js Express gateway
│   ├── src/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── app.js
│   │   └── server.js
│
├── transaction-service/      # FastAPI transaction service
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repository/
│   │   ├── schemas/
│   │   └── services/
│   │
│   └── run.py
│
└── database/
    └── init.sql
```

## API Endpoints
### Gateway
- `POST /transfers` — create a transfer
- `GET /transfers/{id}` — fetch transfer by id
- `GET /transfers` — list transfers
- `GET /health` — gateway health check

### Transaction Service
- `POST /api/transfers/`
- `GET /api/transfers/{transfer_id}`
- `GET /api/transfers/`

## Sample requests/responses
### Example Request
```http
POST /transfers
Idempotency-Key: test-transfer-001
Content-Type: application/json

{
  "from_account": "11111111-1111-1111-1111-111111111111",
  "to_account": "22222222-2222-2222-2222-222222222222",
  "amount": "30.00"
}
```

### Example Response
```http
{
  "id": "transfer-uuid",
  "from_account": "11111111-1111-1111-1111-111111111111",
  "to_account": "22222222-2222-2222-2222-222222222222",
  "amount": "30.00",
  "status": "completed",
  "idempotency_key": "test-transfer-001"
}
```

## Tech Stack
- **Node.js / Express** - API gateway
- **Python / FastAPI** - transaction service
- **PostgreSQL** - persistent data store
- **SQLAlchemy** - ORM and database interaction
- **Docker** - containerisation

## Future Improvements
- Docker Compose orchestration for gateway, service, and database
- automated integration tests
- structured request correlation ids
- account creation and account lookup endpoints
- improved deployment and environment management

## Run Locally

### 1. Start PostgreSQL
Ensure PostgreSQL is running, the database is created and seeded.

### 2. Configure environment variables

#### Gateway `.env`
```env
PORT=3000
TRANSACTION_SERVICE_URL=http://127.0.0.1:8000
TRANSACTION_SERVICE_API_KEY=your-dev-key
```

### 3. Start transaction service
```bash
cd transaction-service
python run.py
```

### 4. Start the gateway
```bash
cd gateway
npm install
npm run dev
```
