# Build Guide for Developers

This guide helps developers set up and build Shadow Farmer locally.

## Prerequisites

- Python 3.12+ (check with `python --version`)
- Node.js 18+ (`node --version`)
- Poetry (`pip install poetry`)
- Docker & Docker Compose
- Git

## Local Development Setup

1. **Clone and Navigate**
   ```bash
   git clone https://github.com/yourusername/shadow-farmer.git
   cd shadow-farmer
   ```

2. **Backend Setup**
   ```bash
   poetry install
   cp .env.example .env  # Fill in API keys, DB URLs
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install --legacy-peer-deps
   cd ..
   ```

4. **Database**
   ```bash
   docker-compose up db redis -d
   alembic upgrade head
   python -c "from app.db.seed import seed_data; seed_data()"
   ```

5. **Run Services**
   ```bash
   # Terminal 1: Backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2: Frontend
   cd frontend && npm run dev

   # Terminal 3: Worker
   celery -A app.workers.farming_tasks worker --loglevel=info
   ```

6. **Verify**
   - Backend: http://localhost:8000/docs (Swagger)
   - Frontend: http://localhost:3000
   - Test API: `curl http://localhost:8000/api/v1/health`

## Code Structure

- `app/`: Backend code (FastAPI, domain, infra)
- `frontend/`: React app
- `tests/`: Pytest for backend, Vitest for frontend
- `alembic/`: DB migrations

## Development Workflow

1. **Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Code Changes**
   - Follow type hints, async/await.
   - Add tests for new features.
   - Update models/migrations if needed.

3. **Testing**
   ```bash
   pytest  # Backend
   cd frontend && npm test  # Frontend
   ```

4. **Linting**
   ```bash
   black app/  # Format
   flake8 app/  # Lint
   cd frontend && npm run lint
   ```

5. **Commit**
   ```bash
   git add .
   git commit -m "feat: add new strategy"
   ```

6. **Push & PR**
   - Push branch, create PR.
   - CI runs tests, linting.

## Debugging

- Backend: Use `print` or logging, check logs.
- Frontend: React DevTools, console.
- Browser: Inspect stealth browser with `headless=False`.
- DB: Connect via pgAdmin or `psql`.

## Building for Production

- Backend: `poetry build`
- Frontend: `npm run build`
- Docker: `docker-compose build`

See DEPLOYMENT.md for deployment.

## Common Issues

- Import errors: Ensure `PYTHONPATH=.`
- DB connection: Check .env DATABASE_URL
- WalletConnect: Verify project ID
- CAPTCHAs: Test CapSolver key

## Contributing

See CONTRIBUTING.md for guidelines.
