# FurFinds Backend

## Overview

FurFinds backend is a FastAPI service providing authentication, pet management, adoption workflows, recommendation APIs, analytics, admin controls, and realtime adoption events.

It is built with SQLite + SQLAlchemy + Alembic, follows OpenAPI standards, and uses dependency injection for database session handling.

## What This Backend Handles

- User registration/login with JWT token issuance
- Pet CRUD and adoption workflows
- Duplicate adoption prevention (business rule)
- Attribute-based recommendation endpoints
- Analytics aggregation for dashboard charts
- Admin-only routes for privileged operations
- WebSocket broadcasts for adoption updates

## Folder Structure

```text
backend/
├─ main.py                  # FastAPI app setup, middleware, router registration
├─ database.py              # SQLAlchemy engine/session/base and DB path config
├─ models.py                # ORM models (users, pets)
├─ schemas.py               # Pydantic request/response contracts
├─ crud.py                  # Data access + business logic helpers
├─ security.py              # Password hashing and JWT encode/decode
├─ dependencies.py          # Auth dependencies and role guards
├─ ai_recommender.py        # Recommendation scoring + optional vector/LLM enhancement
├─ realtime.py              # WebSocket connection manager
├─ routers/                 # Endpoint modules
│  ├─ auth.py
│  ├─ pets.py
│  ├─ admin.py
│  ├─ analytics.py
│  ├─ recommend.py
│  └─ ws.py
├─ alembic/                 # Migration config and revisions
│  └─ versions/
└─ tests/                   # Pytest-based backend tests
```

## Admin Access (Pre-Seeded)

- Email: [admin@furfinds.com](mailto:admin@furfinds.com)
- Password: `Admin@123`

Admin user is pre-seeded via migration and can access admin-only APIs/UI.

## Run Methods

### Method 1: Scripts (Recommended)

From project root:

```bash
setupdev.bat
runapplication.bat
```

Script behavior relevant to backend:

- Creates/uses virtual environment
- Installs dependencies
- Runs `alembic upgrade head`
- Launches backend from `backend/` with `uvicorn main:app --reload`

### Method 2: Manual Backend + Frontend Run

Backend:

```bash
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

Frontend (for full-stack usage):

```bash
cd frontend
npm install
npm run dev
```

### Method 3: Minimal Run (Quick Start)

If environment/dependencies already exist:

```bash
cd backend
uvicorn main:app --reload
```

```bash
cd frontend
npm run dev
```

### Method 4: SDK Regeneration/Usage

With backend running locally:

```bash
npm install -g @openapitools/openapi-generator-cli
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o pet_sdk
```

## API Endpoints

### Auth

- `POST /auth/register` - create user account
- `POST /auth/login` - login and receive JWT

### Pets (Core CRUD + Adoption)

- `POST /pets/` - add pet
- `GET /pets/` - list/filter pets
- `GET /pets/{id}` - get pet by id
- `PUT /pets/{id}` - update pet
- `DELETE /pets/{id}` - delete pet
- `POST /pets/{id}/adopt` - adopt pet

### Recommendation

- `POST /pets/recommend` - recommendation by preferences
- `POST /recommend` - alternate recommendation route

### Analytics

- `GET /analytics` - adoption and distribution metrics

### Admin

- `GET /admin/users` - admin-only user listing

### Realtime

- `WS /ws` - adoption event stream

## Business Logic Enforcement

- Adoption of an already adopted pet is rejected.
- Adoption endpoint returns a domain error converted into proper HTTP response.
- Role-restricted dependencies protect admin APIs.
- Input validation is enforced through Pydantic models.

## Database And Migrations

- DB engine: SQLite
- DB file: `backend/pets.db` (deterministic backend-local path)
- Migrations: Alembic (`backend/alembic/versions/`)
- Upgrade command:

```bash
cd backend
alembic upgrade head
```

- Reset/recreate (development only): drop DB file + rerun migrations.

## Seed Data Notes

- Production-like demo data is generated through `backend/seed_pets.py`.
- It inserts 200 realistic Tamil Nadu pet records via API-level flow.
- Optional SQL seed file can be added if course rubric strictly requires `seed_data.sql`.

## Error Handling And Edge Cases

- Duplicate adoption attempt -> rejected
- Invalid request bodies -> 422 validation responses
- Unauthorized/invalid token -> auth error responses
- Router-level exception handling prevents unhandled crashes for known failure paths

## Testing

From `backend/`:

```bash
pytest
```

What is tested:

- Register/login flow
- Pet CRUD
- Filtering behavior
- Adoption success + duplicate adoption rejection
- Access control scenarios

## OpenAPI

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

## Assignment Alignment

- FastAPI backend and SQLite persistence implemented
- Required endpoints (`POST /pets/`, `POST /pets/{id}/adopt`) implemented
- OpenAPI docs accessible and SDK can be generated from API schema
- Error handling and dependency injection used
- Unit tests included with `pytest`
- Duplicate adoption prevention enforced as required trick logic
