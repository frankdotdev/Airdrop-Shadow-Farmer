# Backend Guide

This guide covers the FastAPI backend of Shadow Farmer.

## Tech Stack

- **Framework**: FastAPI (async, auto-docs)
- **ORM**: SQLAlchemy (async)
- **Queue**: Celery + Redis
- **Blockchain**: Web3.py, Solana-py
- **Security**: Cryptography, JWT
- **Config**: Pydantic from .env

## Project Structure

```
app/
├── api/v1/endpoints/        # Route handlers
│   ├── wallet_routes.py     # Wallet CRUD
│   ├── farming_routes.py    # Task management
│   ├── payment_routes.py    # Subscriptions
│   └── scanner_routes.py    # Airdrop scanning
├── core/                    # Shared utilities
│   ├── config.py            # Settings
│   ├── security.py          # Encryption, JWT
│   ├── humanizer.py         # Randomization
│   ├── scheduler.py         # Periodic tasks
│   └── exceptions.py        # Custom errors
├── domain/                  # Business logic
│   ├── entities/            # Models
│   ├── strategies/          # Farming logic
│   └── scanner.py           # Airdrop polling
├── infrastructure/          # External services
│   ├── blockchain/          # Web3 clients
│   ├── database/            # DB session
│   └── stealth/             # Browser automation
├── workers/                 # Async tasks
│   └── farming_tasks.py     # Celery jobs
└── main.py                  # App entry
```

## Key Components

### API Endpoints
- `/api/v1/wallets/`: List, add, update wallets.
- `/api/v1/farm/`: Start farming tasks.
- `/api/v1/scan/`: Get airdrop opportunities.
- `/api/v1/payment/`: Handle subscriptions.

### Workers
- Celery tasks for farming: Bridge, swap, etc.
- Scheduler for health tasks.

### Security
- JWT auth for users.
- AES-256 for sessions.
- Rate limiting.

## Development

### Setup
```bash
poetry install
cp .env.example .env
docker-compose up db redis -d
alembic upgrade head
python -c "from app.db.seed import seed_data; seed_data()"
uvicorn app.main:app --reload
```

### Testing
- `pytest` for unit/integration.
- Mock blockchain calls.

### Deployment
- Docker: `docker-compose up`
- Scaling: Multiple workers.

## Best Practices

- Async everywhere.
- Type hints.
- Logging with JSON.
- Error handling with custom exceptions.

See README_FOR_DEVELOPERS.md for more.
