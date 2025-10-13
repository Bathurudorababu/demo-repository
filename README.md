# Calorie Tracker Web App (MVP)

Production-ready full-stack calorie tracker with FastAPI, MongoDB, and React + Vite.

## Quick Start (Docker)

1. Copy `.env.example` to `.env` and update secrets if needed
2. Run:

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend:  http://localhost:8000
- MongoDB:  mongodb://localhost:27017

Seed user: `test@example.com` / `password123`

## Tech Stack
- Backend: FastAPI, Motor (MongoDB), JWT
- Frontend: React + Vite + Tailwind, React Query, Recharts
- Docker: Compose services for frontend, backend, mongo

## Backend

- Path: `backend/`
- Run locally:

```bash
pip install -r backend/requirements.txt
uvicorn app.main:app --reload
```

### API

- Auth: POST `/api/v1/auth/register`, POST `/api/v1/auth/login`, GET `/api/v1/auth/me`, PATCH `/api/v1/auth/update`
- Foods: GET `/api/v1/foods?query=apple`, GET `/api/v1/foods/{id}`, POST `/api/v1/foods` (admin)
- Meals: POST `/api/v1/meals`, GET `/api/v1/meals?date=YYYY-MM-DD`, DELETE `/api/v1/meals/{meal_id}`
- Goals: POST `/api/v1/goals`, GET `/api/v1/goals`
- Analytics: GET `/api/v1/analytics/summary`, GET `/api/v1/analytics/trends`

Responses use a uniform model:

```json
{
  "status": "success",
  "message": "Data retrieved successfully",
  "data": { }
}
```

### Tests

```bash
cd backend
pytest -q
```

## Frontend

- Path: `frontend/`
- Development:

```bash
cd frontend
npm i
npm run dev
```

Set `VITE_API_URL` env to backend URL.

## Postman

Import `postman/CalorieTracker.postman_collection.json` for endpoints.

## Security & Config

- Set `JWT_SECRET` in `.env`
- CORS origins configured via `CORS_ORIGINS`
- Seeding can be toggled via `SEED=true|false`

## License
MIT
