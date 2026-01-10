# Architecture Overview

Shadow Farmer follows a clean architecture pattern to ensure separation of concerns, scalability, and maintainability. The system is divided into layers: Presentation (API/Frontend), Domain (Business Logic), Infrastructure (External Services), and Core (Shared Utilities).

## Layered Architecture

### 1. Presentation Layer
- **Backend**: FastAPI for REST API endpoints (wallet management, farming tasks, payments, scanning).
- **Frontend**: React with TypeScript, Tailwind CSS, shadcn/ui for UI components, React Router for navigation, WalletConnect v2 for dApp integration, TWA SDK for Telegram Mini App.
- **Communication**: Axios for API calls, WebSockets for real-time updates (e.g., task status).

### 2. Domain Layer
- **Entities**: User, Wallet, Task models with business rules (e.g., referral codes, sybil scores).
- **Strategies**: BaseChainStrategy for EVM/Solana operations, extensible for new chains (e.g., ZKSync).
- **Scanner**: AirdropScanner for polling Coingecko and Twitter.
- **Use Cases**: Farming tasks, profit estimation, subscription management.

### 3. Infrastructure Layer
- **Database**: PostgreSQL with SQLAlchemy ORM, Alembic for migrations.
- **Blockchain**: Web3.py for EVM (Uniswap/Base Bridge), solana-py for Solana (Jupiter swaps).
- **Stealth**: Playwright for browser automation, CapSolver for CAPTCHA, BrightData for proxies.
- **Queue**: Celery with Redis for async tasks (farming, health checks).
- **Caching**: Redis for prices, sessions.

### 4. Core Layer
- **Config**: Pydantic settings from .env.
- **Security**: AES-256 encryption (cryptography), JWT auth (python-jose).
- **Humanizer**: Random delays/jitters to mimic human behavior.
- **Scheduler**: Periodic tasks for farming/health.
- **Exceptions**: Custom errors for graceful handling.

## Data Flow
1. User interacts via TWA frontend → API call to FastAPI.
2. API validates (Pydantic), authenticates (JWT), queries DB.
3. Business logic in Domain (e.g., build tx via Infrastructure clients).
4. Async tasks queued to Celery for execution (e.g., swap tx with Gas Guard).
5. Results cached in Redis, notified via Telegram Bot.
6. Frontend polls/updates UI with Recharts for charts, shadcn for components.

## Scalability
- Horizontal scaling: Multiple Celery workers, Redis cluster.
- Load balancing: Nginx in docker-compose.
- Rate limiting: FastAPI middleware.

## Security
- Secrets in .env, encrypted DB fields.
- Non-custodial: Private keys encrypted, user signs txs via WalletConnect.
- Anti-detection: Proxy rotation, fingerprint spoofing, humanized actions.

## Tech Stack
- Backend: Python 3.12, FastAPI, SQLAlchemy, Celery, Redis.
- Frontend: React 18, TypeScript, Vite, Tailwind, shadcn/ui.
- Blockchain: Web3.py, solana-py.
- Deployment: Docker, PostgreSQL, Nginx.

For detailed code structure, see CODE_GUIDE.md.
