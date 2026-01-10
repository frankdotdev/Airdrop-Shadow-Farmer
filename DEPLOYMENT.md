# Deployment Guide

This guide covers deploying Shadow Farmer to production environments like Render, Railway, or self-hosted.

## Prerequisites

- Docker and Docker Compose installed.
- PostgreSQL database (managed or self-hosted).
- Redis instance (managed or self-hosted).
- Domain/SSL for HTTPS.

## Environment Variables

Create a `.env` file with:

```
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
ALCHEMY_RPC_URL=https://eth-mainnet.alchemyapi.io/v2/YOUR_KEY
INFURA_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
TELEGRAM_BOT_TOKEN=your_bot_token
WALLET_CONNECT_PROJECT_ID=your_wc_project_id
BRIGHTDATA_PROXY_URL=https://your_proxy_url
CAPSOLVER_API_KEY=your_capsolver_key
COINGECKO_API_KEY=your_coingecko_key
ENCRYPTION_KEY=your_32_char_key
```

## Docker Deployment

1. Build and run with Docker Compose:
   ```
   docker-compose up --build -d
   ```

2. Run migrations:
   ```
   docker-compose exec backend alembic upgrade head
   ```

3. Seed data (if applicable):
   ```
   docker-compose exec backend python -c "from app.db.seed import seed_data; seed_data()"
   ```

4. Access at http://localhost:8000 (backend) and http://localhost:3000 (frontend).

## Cloud Deployment

### Render
1. Connect GitHub repo.
2. Create services: PostgreSQL, Redis, Web Service for backend, Static Site for frontend.
3. Set env vars in Render dashboard.
4. Deploy.

### Railway
1. Import from GitHub.
2. Add PostgreSQL and Redis plugins.
3. Set env vars.
4. Deploy.

## Self-Hosted

1. Install Docker on VPS.
2. Clone repo.
3. Run `docker-compose up -d`.
4. Set up Nginx reverse proxy for SSL.

## Monitoring

- Use Sentry for error tracking.
- Monitor with Grafana/Prometheus.
- Logs via Docker logs or ELK stack.

## Scaling

- Scale Celery workers: `docker-compose up --scale worker=N`.
- Use load balancer for multiple instances.
- Cache aggressively with Redis.

## Security

- Use HTTPS everywhere.
- Rotate secrets regularly.
- Enable 2FA for admin access.
- Audit logs for suspicious activity.

For issues, check logs: `docker-compose logs`.
