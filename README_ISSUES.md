# Troubleshooting Guide

This guide helps resolve common issues in Shadow Farmer.

## Backend Issues

### Module Not Found
- Error: `ModuleNotFoundError: No module named 'fastapi'`
- Fix: `poetry install` or `pip install -r requirements.txt`

### DB Connection
- Error: `psycopg2.OperationalError`
- Fix: Check .env DATABASE_URL, ensure Postgres running.

### Alembic Migration
- Error: `alembic upgrade head` fails
- Fix: `alembic revision --autogenerate`, then upgrade.

### Celery Worker
- Error: Worker not picking tasks
- Fix: `celery -A app.workers.farming_tasks worker --loglevel=info`
- Check Redis: `redis-cli ping`

### Web3 RPC
- Error: `Web3Exception: Bad response`
- Fix: Rotate RPC (Alchemy/Infura), check API key.

## Frontend Issues

### React Errors
- Error: `Cannot find module 'react'`
- Fix: `npm install` in frontend/

### WalletConnect
- Error: Connection fails
- Fix: Check project ID in .env, refresh QR.

### API Calls
- Error: 401 Unauthorized
- Fix: Login again, check JWT expiry.

### Build Fails
- Error: TypeScript errors
- Fix: `npm run lint`, fix types.

## General Issues

### Docker
- Error: `docker-compose up` fails
- Fix: `docker system prune`, rebuild.

### Ports Conflict
- Error: Port 8000 in use
- Fix: Change in docker-compose.yml or kill process.

### High Gas
- Issue: Tx failing due to gas
- Fix: Enable Gas Guard, wait for lower prices.

### CAPTCHA
- Issue: Solving fails
- Fix: Check CapSolver key, manual solve.

### Sybil Score High
- Issue: Farming blocked
- Fix: Use fresh wallet, reduce activity.

### Payments
- Issue: Subscription not activating
- Fix: Check tx on Etherscan, contact support.

## Logs

- Backend: `docker-compose logs backend`
- Frontend: Browser console
- Worker: Celery logs

## Support

- GitHub Issues for bugs
- Discord for community help
- Email: support@shadowfarmer.com

## Prevention

- Test on testnets first
- Backup DB regularly
- Monitor resources
