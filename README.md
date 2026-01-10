# Shadow Farmer

A Telegram Mini App for automated airdrop farming in Web3, designed to mimic human behavior and bypass detection.

## Features

- Non-custodial automation using WalletConnect v2
- Human-like randomization to avoid bans
- Multi-chain support (EVM, Solana)
- Sybil score checker
- Gas guard with dynamic pricing
- Auto CAPTCHA solving via CapSolver
- Subscription tiers (Hobbyist, Whales, Protocol)
- Airdrop scanner (Coingecko, Twitter)
- Telegram notifications
- Stealth browser with proxy rotation

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL & Redis (or use Docker)

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/shadow-farmer.git
   cd shadow-farmer
   ```

2. **Install dependencies**
   ```bash
   poetry install
   cd frontend && npm install --legacy-peer-deps && cd ..
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your keys (DATABASE_URL, RPCs, API keys, etc.)
   ```

4. **Database setup**
   ```bash
   docker-compose up db redis -d
   alembic upgrade head
   python -c "from app.db.seed import seed_data; seed_data()"
   ```

5. **Run the app**
   ```bash
   # Backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Frontend (new terminal)
   cd frontend && npm run dev

   # Celery worker (new terminal)
   celery -A app.workers.farming_tasks worker --loglevel=info
   ```

6. **Access**
   - Backend API: http://localhost:8000/docs
   - Frontend: http://localhost:3000

### Docker Deployment

```bash
docker-compose up --build -d
# Access at http://localhost:8000 (backend) and http://localhost:3000 (frontend)
```

For production, see [DEPLOYMENT.md](DEPLOYMENT.md).

## API Endpoints

- `GET /api/v1/wallets/list/{user_id}` - List wallets
- `POST /api/v1/wallets/add` - Add wallet
- `POST /api/v1/farm/run` - Start farming task
- `GET /api/v1/scan` - Scan airdrops
- `POST /api/v1/payment/subscribe` - Subscribe

Full docs at `/docs`.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for layered design.

## Security

See [SECURITY.md](SECURITY.md) for encryption, anti-detection, etc.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Disclaimer

Use at your own risk. Airdrop farming may violate terms of service. Non-custodial, but test on testnets first.
