# Scaling Guide

This guide covers scaling Shadow Farmer for high traffic and user load.

## Current Architecture

- Backend: FastAPI (async), Celery workers, Redis queue.
- DB: PostgreSQL.
- Frontend: React SPA.
- Hosting: Docker containers.

## Performance Bottlenecks

1. **API Requests**: FastAPI handles 1000+ req/s, but DB queries slow.
2. **Blockchain Calls**: RPC rate limits (Alchemy/Infura).
3. **Browser Automation**: Playwright instances resource-intensive.
4. **DB**: Read-heavy, needs indexing.

## Scaling Strategies

### 1. Horizontal Scaling

- **API Servers**: Run multiple FastAPI instances behind Nginx load balancer.
  ```yaml
  # docker-compose.yml
  services:
    api:
      scale: 3  # 3 instances
  ```

- **Workers**: Scale Celery workers.
  ```bash
  docker-compose up --scale worker=5
  ```

- **DB**: Read replicas for queries.
  ```yaml
  services:
    db-replica:
      image: postgres
      command: ["postgres", "-c", "hot_standby=on"]
  ```

### 2. Caching

- **Redis**: Cache prices, user data, API responses.
  ```python
  from redis import Redis
  cache = Redis(host='redis')
  ```

- **CDN**: Cloudflare for static assets.

### 3. Database Optimization

- **Indexing**: Add indexes on user_id, address, status.
  ```sql
  CREATE INDEX idx_wallet_user ON wallets(user_id);
  ```

- **Partitioning**: Partition tasks by date.
- **Connection Pooling**: SQLAlchemy pool.

### 4. Async & Concurrency

- Use async/await for I/O.
- Limit concurrent browser instances (max 10 per worker).
- Batch DB inserts.

### 5. External Limits

- **RPC**: Rotate providers (Alchemy, Infura, custom nodes).
- **APIs**: Cache Coingecko responses (1min TTL).
- **Proxies**: Pool of residential IPs.

### 6. Monitoring

- **Metrics**: Prometheus for CPU, memory, req/s.
- **Logs**: ELK stack or CloudWatch.
- **Alerts**: High gas prices, failed txs.

## Load Testing

- Use Locust or Artillery.
- Simulate 1000 users farming.
- Measure latency, throughput.

## Cost Optimization

- **Serverless**: AWS Lambda for API (but Celery needs EC2).
- **Spot Instances**: For workers.
- **Auto-scaling**: Kubernetes HPA based on queue length.

## Future Scaling

- **Microservices**: Split scanner, farming into services.
- **Event-Driven**: Kafka for tx events.
- **Global CDN**: For low-latency.

## Benchmarks

- 1 worker: 10 farms/min
- 10 workers: 100 farms/min
- Target: 1000+ concurrent users.

Monitor and iterate based on usage.
