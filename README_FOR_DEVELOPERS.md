# Developer Guide

This guide is for developers contributing to Shadow Farmer's codebase.

## Architecture Overview

Shadow Farmer uses Clean Architecture:
- **Presentation**: API routes, TWA frontend.
- **Domain**: Business logic, entities, strategies.
- **Infrastructure**: Blockchain clients, DB, external APIs.
- **Core**: Config, security, utilities.

## Key Components

### Backend (Python/FastAPI)

- **Models**: SQLAlchemy ORM in `app/infrastructure/database/models.py`
- **Routes**: `app/api/v1/endpoints/` (wallets, farming, payments, scanner)
- **Workers**: Celery tasks in `app/workers/farming_tasks.py`
- **Clients**: EVM (`web3_client.py`), Solana (`solana_client.py`)
- **Stealth**: Browser automation in `app/stealth/browser.py`
- **Domain**: Strategies in `app/domain/strategies/`, Scanner in `app/domain/scanner.py`

### Frontend (React/TypeScript)

- **Components**: Dashboard, Wallets, Strategies in `frontend/src/components/`
- **Hooks**: WalletConnect in `frontend/src/hooks/`
- **Context**: Auth via TWA SDK in `frontend/src/contexts/`
- **Styling**: Tailwind + shadcn/ui

## Coding Standards

- **Python**: Type hints, async/await, Black formatting, flake8 linting.
- **TypeScript**: Strict types, ESLint, Prettier.
- **Commits**: Conventional (feat:, fix:, docs:).
- **Tests**: Pytest for backend, Vitest for frontend.

## Adding Features

### New Strategy
1. Create `app/domain/strategies/new_strategy.py` inheriting `BaseChainStrategy`.
2. Implement `execute()` method.
3. Add to `farming_tasks.py`.
4. Update frontend Strategies component.

### New API Endpoint
1. Add route in `app/api/v1/endpoints/new_routes.py`.
2. Register in `app/main.py`.
3. Add Pydantic models in `app/domain/entities/`.
4. Test with pytest.

### Frontend Component
1. Create in `frontend/src/components/`.
2. Use shadcn/ui for UI.
3. Integrate with axios for API calls.
4. Add to router in `App.tsx`.

## Testing

- **Unit Tests**: Test functions in isolation.
- **Integration**: Test API endpoints, DB interactions.
- **E2E**: Playwright for browser flows.
- Run: `pytest` or `npm test`.

## Security Considerations

- Never log sensitive data.
- Encrypt DB fields.
- Validate inputs.
- Use HTTPS.

## Performance

- Cache with Redis.
- Async operations.
- Optimize DB queries.

## Deployment

- Use Docker for consistency.
- CI/CD with GitHub Actions.
- Monitor with logs, Sentry.

## Resources

- FastAPI docs: https://fastapi.tiangolo.com/
- React docs: https://react.dev/
- Web3.py: https://web3py.readthedocs.io/
- Solana-py: https://michaelhly.github.io/solana-py/

For questions, open an issue or discuss in PRs.
