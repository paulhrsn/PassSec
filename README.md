# PassSec

PassSec is a full-stack Security+ quiz trainer with authentication, domain-focused quizzes, and progress analytics.

## Stack

- Backend: Flask, SQLAlchemy, JWT, Bcrypt
- Frontend: React + Vite + Tailwind + Recharts
- DB: SQLite (local dev) or PostgreSQL (production)

## What is production-ready now

- Stronger backend config validation (`SECRET_KEY` and `JWT_SECRET_KEY` are required)
- JWT auth hardened with standardized error responses and expiration window
- Safer quiz question storage (`JSON` instead of `PickleType`)
- Input validation improved for auth and quiz submission payloads
- Added `/api/me` endpoint for session verification
- Added `/api/quiz/domains` endpoint for dynamic frontend domain selection
- Frontend route protection now verifies server-side session state
- Frontend build/lint and backend app startup validated

## Local development

### 1. Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Update values in `.env`:

- `SECRET_KEY`: long random string
- `JWT_SECRET_KEY`: long random string
- `DATABASE_URL`: use SQLite for local dev or PostgreSQL URL
- `CORS_ORIGINS`: frontend origin(s), comma-separated

### 2. Create DB and seed quiz data

```bash
cd backend
source .venv/bin/activate
python setup_db.py
python seed/seed_quiz_data.py
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Run backend

```bash
cd backend
source .venv/bin/activate
flask --app run.py run --port 5001
```

Frontend expects backend at `http://localhost:5001/api` by default.

## Production deployment

## Option A (recommended): Render + Vercel

### Backend on Render

1. Create a new Web Service from the repo.
2. Set root directory to `backend`.
3. Build command:

```bash
pip install -r requirements.txt
```

4. Start command:

```bash
gunicorn run:app
```

5. Add environment variables:

- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL` (managed PostgreSQL recommended)
- `CORS_ORIGINS` (set to your frontend URL)
- `JWT_EXPIRES_HOURS` (for example `12`)

### Frontend on Vercel

1. Import repo into Vercel.
2. Set project root to `frontend`.
3. Add env var:

- `VITE_API_BASE=https://<your-render-service>.onrender.com/api`

4. Deploy.

Then set backend `CORS_ORIGINS` to your Vercel domain.

## Option B: Railway + Netlify

- Railway for backend+Postgres, Netlify for frontend
- Same env var pattern as above

## First live link checklist

1. Confirm backend health: `GET /api/health` returns `{"status":"OK"}`.
2. Confirm frontend can register/login.
3. Confirm quiz loads domains from `/api/quiz/domains`.
4. Confirm quiz submission updates dashboard stats.
5. Confirm CORS allows only your frontend origin.

## Useful commands

```bash
# frontend quality checks
cd frontend && npm run lint && npm run build

# backend smoke check
cd backend && source .venv/bin/activate && python -c "from app import create_app; create_app()"
```

## Notes

- Keep `.env` out of git.
- Rotate secrets if they were ever exposed.
- Prefer managed PostgreSQL in production.
