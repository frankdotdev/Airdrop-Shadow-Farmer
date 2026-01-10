# Contributing Guide

We welcome contributions! Follow these steps to contribute to Shadow Farmer.

## Development Setup

1. Fork the repo.
2. Clone: `git clone https://github.com/yourusername/shadow-farmer.git`
3. Install: `poetry install && cd frontend && npm install`
4. Set up .env (copy from .env.example).
5. Run DB: `docker-compose up db redis -d`
6. Migrate: `alembic upgrade head`
7. Start: `uvicorn app.main:app --reload` and `cd frontend && npm run dev`

## Code Style

- Backend: Black, isort, flake8.
- Frontend: ESLint, Prettier.
- Commit messages: Conventional commits (feat:, fix:, docs:).

## Testing

- Backend: `pytest`
- Frontend: `npm test`
- E2E: Playwright for browser tests.

## Pull Requests

1. Create feature branch: `git checkout -b feature/your-feature`
2. Write tests.
3. Ensure CI passes.
4. Update docs if needed.
5. Submit PR with description.

## Security

- Never commit secrets.
- Use encrypted fields for sensitive data.
- Report vulnerabilities privately.

## Issues

- Use GitHub Issues for bugs/features.
- Provide steps to reproduce, expected vs actual behavior.

## Code of Conduct

Be respectful and inclusive. No harassment.

Thank you for contributing!
