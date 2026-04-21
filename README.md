# FurFinds
## Find. Adopt. Love.

FurFinds is a full-stack pet adoption platform that combines a FastAPI backend, React frontend, SQLite database, OpenAPI-based SDK, analytics, and AI-assisted recommendations.

This repository is structured to be understandable by both humans and AI agents, and to be runnable with either scripts or manual commands.

## What The System Does

- Lets users register/login and browse pets through API-driven flows.
- Supports full pet lifecycle operations: create, view, update, delete, adopt.
- Prevents duplicate adoption through backend business logic enforcement.
- Provides advanced filtering, analytics charts, admin controls, and AI recommendations.
- Sends real-time adoption updates over WebSocket.

## Why FurFinds Is Unique

- Uses a realistic Tamil Nadu-focused dataset (200 pets) for demo realism.
- AI recommendation logic considers city, type, breed, vaccination, sterilization, and description hints.
- Includes a complete ecosystem: backend + frontend + migrations + tests + generated Python SDK + automation scripts.

## Core Features

- JWT authentication (`/auth/register`, `/auth/login`)
- Pet CRUD + adoption workflow
- Duplicate adoption prevention (cannot adopt the same pet twice)
- Advanced multi-filter pet discovery
- Analytics dashboard with charts (type/city/adoption/vaccination/age)
- Admin control panel for user visibility and pet management
- AI recommendation page with reasoning output
- Real-time pet adoption updates via WebSocket

## Tech Stack

- Backend: FastAPI, SQLAlchemy, SQLite, Alembic, Pytest
- Frontend: React (Vite), Axios, React Router, Chart.js
- SDK: OpenAPI Generator Python client (`pet_sdk/`)
- Runtime: Windows batch automation scripts

## Project Structure

```text
FurFinds/
├─ backend/                 # FastAPI app: routers, schemas, models, auth, AI, realtime
│  ├─ alembic/              # Database migration environment and versioned revisions
│  ├─ routers/              # Route modules: auth, pets, admin, analytics, recommend, ws
│  └─ tests/                # Backend unit/integration tests (pytest)
├─ frontend/                # React app: pages, layout, protected routes, API client
├─ pet_sdk/                 # Generated Python SDK from OpenAPI spec
├─ setupdev.bat             # One-time setup script for backend/frontend dependencies + migrations
├─ runapplication.bat       # Launch script for backend + frontend
├─ openapi.json             # OpenAPI artifact (regenerate from running backend as needed)
└─ README.md                # Root project guide
```

## Admin Access (Pre-Seeded)

- Email: [admin@furfinds.com]
- Password: `Admin@123`

Admin user is pre-seeded through migrations and is used to access the admin panel.

## Run Methods

### Method 1: Scripts (Recommended)

From repository root:

```bash
setupdev.bat
runapplication.bat
```

What scripts do:

- `setupdev.bat`
  - Creates Python virtual environment (`.venv`)
  - Installs backend dependencies
  - Runs `alembic upgrade head`
  - Installs frontend dependencies
- `runapplication.bat`
  - Validates required files/tools
  - Starts backend from `backend/`
  - Runs migrations before backend boot
  - Starts frontend dev server

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

Frontend:

```bash
cd frontend
npm install
npm run dev
```

### Method 3: Minimal Run (Quick Start)

For already configured environments:

```bash
cd backend
uvicorn main:app --reload
```

```bash
cd frontend
npm run dev
```

### Method 4: SDK Generation/Usage

Generate SDK from running backend:

```bash
npm install -g @openapitools/openapi-generator-cli
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o pet_sdk
```

Example usage:

```python
from pet_sdk.api.pets_api import PetsApi
from pet_sdk import ApiClient

client = ApiClient()
api = PetsApi(client)
# result = api.list_pets_pets__get()
```

## OpenAPI / Docs

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

## Error Handling And Edge Cases

- Duplicate adoption attempts are blocked with domain-safe API errors.
- Invalid payloads return validation errors (4xx) through FastAPI/Pydantic.
- Frontend renders API errors safely without crashing pages.
- Auth-protected routes reject unauthorized requests cleanly.

## Testing

From `backend/`:

```bash
pytest
```

Test coverage includes:

- Register/login flows
- Pet create/read/update/delete
- Filter behavior
- Adoption success and duplicate-adoption rejection
- Authorization and admin route behavior

## Assignment Alignment

This implementation satisfies the challenge requirements:

- FastAPI backend with OpenAPI-compliant endpoints
- SQLite database with Alembic migrations
- React frontend using Axios-only API integration
- Platform SDK generation via OpenAPI Generator CLI
- Setup and run scripts (`setupdev.bat`, `runapplication.bat`)
- Backend tests with `pytest`
- Business logic enforcement (no re-adoption)
- Bonus capabilities: analytics, AI recommendations, real-time updates, richer admin UX

## Additional Guides

- Backend details: `backend/README.md`
- Frontend details: `frontend/README.md`
