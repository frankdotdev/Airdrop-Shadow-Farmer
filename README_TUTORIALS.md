# Tutorials

This guide provides tutorials for frontend, backend, and database.

## Backend Tutorial

### 1. Setup
```bash
poetry install
uvicorn app.main:app --reload
```

### 2. Add Endpoint
- Create `app/api/v1/endpoints/new.py`
- Add route: `@router.get("/new")`
- Register in `main.py`

### 3. DB Model
- Add to `models.py`
- Migrate: `alembic revision --autogenerate`

### 4. Test
- `pytest tests/test_new.py`

## Frontend Tutorial

### 1. Setup
```bash
cd frontend
npm install
npm run dev
```

### 2. Component
- Create `src/components/New.tsx`
- Use hooks: `useState`, `useEffect`

### 3. API Call
- `axios.get('/api/v1/new')`

### 4. Style
- Tailwind: `className="bg-blue-500"`

## Database Tutorial

### 1. Connect
- `from app.infrastructure.database import get_db`

### 2. Query
- `db.query(User).filter(User.id == 1).first()`

### 3. Migrate
- `alembic upgrade head`

### 4. Seed
- Run `seed.py`

## Advanced

- Async: Use `async def`
- Auth: JWT in headers
- Deploy: Docker

Practice with small changes.
