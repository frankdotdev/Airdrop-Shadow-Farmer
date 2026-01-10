# Database Guide

This guide covers the PostgreSQL database setup and management for Shadow Farmer.

## Schema

### Tables

- **users**: id, telegram_id, subscription_tier, referral_code, referred_by, created_at
- **wallets**: id, user_id, address, encrypted_session, proxy_ip, sybil_score, profit_estimate, last_activity
- **tasks**: id, wallet_id, status, type, created_at, completed_at

### Relationships
- User 1:N Wallets
- Wallet 1:N Tasks
- Self-referencing: User.referrals

## Setup

### Local
```bash
docker run --name postgres -e POSTGRES_PASSWORD=pass -p 5432:5432 -d postgres
createdb shadow_farmer
```

### Migrations
- Tool: Alembic
- Init: `alembic init alembic`
- Create: `alembic revision -m "add models"`
- Run: `alembic upgrade head`

## Queries

### Common
- Get user wallets: `SELECT * FROM wallets WHERE user_id = ?`
- Update profit: `UPDATE wallets SET profit_estimate = ? WHERE id = ?`
- Task status: `SELECT status FROM tasks WHERE id = ?`

### Optimization
- Indexes: `CREATE INDEX idx_wallet_user ON wallets(user_id);`
- Views: For aggregated profits.
- Partitioning: Tasks by month.

## Connection

- Library: SQLAlchemy async
- Pool: 10 connections
- URL: `postgresql://user:pass@host/db`

## Seeding

- Script: `app/db/seed.py`
- Run: `python -c "from app.db.seed import seed_data; seed_data()"`
- Data: Admin user, sample wallet.

## Backup

- Command: `pg_dump shadow_farmer > backup.sql`
- Restore: `psql shadow_farmer < backup.sql`
- Automated: Cron job daily.

## Monitoring

- Slow queries: `pg_stat_statements`
- Connections: `pg_stat_activity`
- Size: `SELECT pg_size_pretty(pg_database_size('shadow_farmer'));`

## Scaling

- Read replicas: For queries.
- Sharding: By user region.
- Caching: Redis for hot data.

## Security

- Encrypted fields: Use pg_crypto for sensitive data.
- Access: Least privilege roles.
- Audit: Enable logging.

See README_BACKEND.md for integration.
