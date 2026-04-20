# FurFinds
### Find. Adopt. Love.

FurFinds is a full-stack pet adoption platform built end-to-end by a single developer.  
It demonstrates backend API design, database migrations, authentication, frontend UX, analytics visualization, and practical AI-assisted recommendations in one integrated system.

## Project Overview

FurFinds is built with FastAPI, React, and SQLite, and includes:
- pet management and adoption workflow
- JWT authentication and role-based access
- rich pet profiles with Tamil Nadu city context
- dynamic filtering and smart recommendations
- analytics dashboards with multiple charts
- WebSocket real-time adoption updates
- generated OpenAPI Python SDK

## Features

### Core
- View, add, and adopt pets
- Prevent duplicate adoption using business rules

### Authentication
- User registration and login with JWT
- Protected routes and role-based checks

### Admin
- Pre-seeded admin account
- Admin-only endpoint for user listing

### Pet System
- Rich pet profile fields (breed, age, gender, health, location, contact)
- Multi-filter pets page (type, city, vaccination, sterilization, etc.)

### AI Recommendation
- Attribute-based scoring using city, pet type, health status, and description
- Supports natural language preference input

### Analytics
- Adoption rate (adopted vs available)
- Pets by type
- Pets by city (Tamil Nadu focus)
- Vaccination status
- Age distribution

### Real-Time
- WebSocket broadcast on adoption updates

### Extras
- OpenAPI-generated Python SDK (`pet_sdk/`)
- Setup and run automation scripts

## Tamil Nadu Context

The project is localized with realistic Tamil Nadu context:
- Cities include `Chennai`, `Coimbatore`, `Madurai`, `Erode`, and `Salem`
- Filters, analytics labels, and seeded/normalized data reflect these locations
- Phone numbers are normalized with `+91` format for pet contact records

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pytest

### Frontend
- React (Vite)
- Axios
- React Router
- Chart.js (`react-chartjs-2`)

### Auth
- JWT (`pyjwt`)
- `bcrypt`

## Project Structure

```text
FurFinds/
  main.py, models.py, schemas.py, crud.py, ...
  routers/                    # API route modules
  alembic/                    # DB migrations
  tests/                      # backend tests
  frontend/                   # React app
  pet_sdk/                    # generated Python SDK
  setupdev.bat                # setup script
  runapplication.bat          # full app launcher
```

Logical grouping:
- `backend/` -> implemented at repository root (`main.py`, `routers/`, `models.py`, etc.)
- `frontend/` -> React UI
- `alembic/` -> migration history
- `tests/` -> test suite
- `pet_sdk/` -> generated client SDK
- `scripts/` -> represented by root batch scripts

## How To Run

### 1) Clone

```bash
git clone <repo_url>
cd FurFinds
```

### 2) Setup (recommended)

```bat
setupdev.bat
```

This installs backend and frontend dependencies and runs migrations.  
Database files are not required in git; migrations recreate schema after clone.

### 3) Run Entire Application

```bat
runapplication.bat
```

Starts backend and frontend in separate terminal windows.

## Run Modes (Clear Options)

### Backend Only

```bat
call .venv\Scripts\activate.bat
python -m uvicorn --app-dir . main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Only

```bat
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

### Full App (Single Command)

```bat
runapplication.bat
```

## Access URLs

- Frontend: `http://127.0.0.1:5173`
- Backend docs: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

## Frontend Environment Configuration

Use `frontend/.env` (copy from `frontend/.env.example`):
- `VITE_API_BASE_URL` (default `http://127.0.0.1:8000`)
- `VITE_WS_BASE_URL` (optional; auto-derived when omitted)

## Admin Login

- Email: [admin@furfinds.com](mailto:admin@furfinds.com)
- Password: `Admin@123`

Notes:
- Admin user is pre-seeded via Alembic migration
- Normal users can register through `/auth/register`

## API Overview

Core endpoints:
- `POST /auth/register`
- `POST /auth/login`
- `GET /pets/`
- `POST /pets/`
- `POST /pets/{id}/adopt`

Useful extras:
- `POST /pets/recommend`
- `POST /recommend`
- `GET /analytics`
- `GET /admin/users` (admin only)
- `WS /ws`

Filter query example:
```http
GET /pets/?type=Dog&city=Coimbatore&vaccinated=true
```

## Testing

```bash
pytest
```

or

```bat
python -m pytest -q
```

## Troubleshooting

If full launcher has issues, run services manually:

Backend:
```bat
call .venv\Scripts\activate.bat
python -m uvicorn --app-dir . main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:
```bat
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Re-run migrations:
```bat
call .venv\Scripts\activate.bat
python -m alembic upgrade head
```

## Development Note

This project was designed and implemented end-to-end, covering backend APIs, database design/migrations, authentication/authorization, frontend UX, analytics, AI recommendation logic, and system integration.

## Future Improvements

- Expand recommendation to full RAG pipeline with richer retrieval/ranking
- Production-grade auth hardening (cookies, refresh tokens, stricter session controls)
- Containerized/cloud deployment pipeline (Docker + CI/CD + hosted DB)
