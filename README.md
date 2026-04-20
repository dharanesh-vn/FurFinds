# FurFinds

**Tagline:** Find. Adopt. Love.

FurFinds is a full-stack pet adoption platform with a FastAPI backend, React frontend, Alembic migrations, pytest coverage, and a generated Python SDK.

## Current Implementation Status

- Backend API for pets is implemented (`create`, `list`, `adopt`).
- Adoption business rule is enforced (`400` on re-adoption, `404` on missing pet).
- SQLite schema is managed by Alembic.
- Automated tests are in place and passing.
- React frontend supports:
  - listing pets
  - adding pets
  - adopting pets
- Python SDK is generated from OpenAPI and includes an example usage script.
- Automation scripts are included for setup and startup.

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

### SDK
- OpenAPI Generator CLI (Python client)

## Project Structure

```text
FurFinds/
├─ main.py
├─ database.py
├─ models.py
├─ schemas.py
├─ crud.py
├─ routers/
│  ├─ __init__.py
│  └─ pets.py
├─ alembic/
│  ├─ env.py
│  └─ versions/
├─ tests/
│  └─ test_pets.py
├─ frontend/
│  └─ src/
├─ pet_sdk/
│  ├─ openapi_client/
│  └─ example_usage.py
├─ setupdev.bat
├─ runapplication.bat
└─ README.md
```

## Backend API

Base URL: `http://127.0.0.1:8000`

### Endpoints

- `POST /pets/`
  - Body: `{ "name": "Bruno", "type": "Dog" }`
  - Returns: created pet (`201`)
- `GET /pets/`
  - Returns: list of pets (`200`)
- `POST /pets/{id}/adopt`
  - Returns: updated pet (`200`)
  - Errors:
    - `400` if already adopted
    - `404` if pet does not exist

Swagger docs:
- `http://127.0.0.1:8000/docs`

## Database and Migrations

- DB URL: `sqlite:///./pets.db`
- Alembic config file: `alembic.ini`
- Metadata source: `Base.metadata` via `alembic/env.py`
- Initial migration creates table `pets` with:
  - `id` (PK)
  - `name`
  - `type`
  - `adopted` (`DEFAULT 0`)
  - indexes on `id`, `name`, `type`

### Migration commands

```bat
python -m alembic upgrade head
python -m alembic downgrade -1
```

## Frontend

Frontend folder: `frontend/`

### Features

- Fetches pets from backend (`GET /pets/`)
- Add-pet form (`POST /pets/`)
- Adopt button (`POST /pets/{id}/adopt`)
- Adopt button disables automatically for adopted pets
- Uses `useState` and `useEffect` for state/data flow

### Run frontend only

```bat
cd frontend
npm install
npm run dev
```

Default URL: `http://127.0.0.1:5173`

## Python SDK

SDK output folder: `pet_sdk/`

### Regenerate SDK

1. Export OpenAPI spec:
```bat
python -c "import json; from main import app; open('openapi.json','w',encoding='utf-8').write(json.dumps(app.openapi(), indent=2))"
```

2. Generate SDK:
```bat
npx @openapitools/openapi-generator-cli generate -i openapi.json -g python -o pet_sdk
```

### SDK usage example

```bat
python pet_sdk/example_usage.py
```

`example_usage.py` demonstrates:
- listing pets
- creating a pet if none exist
- adopting a pet

## Automated Scripts

## `setupdev.bat`

Performs:
1. Create `.venv`
2. Install backend dependencies
3. Run `alembic upgrade head`
4. Install frontend dependencies (`frontend/npm install`)

Usage:
```bat
setupdev.bat
```

## `runapplication.bat`

Performs:
1. Validates `.venv`, `python`, `npm`, and frontend files
2. Starts backend in new terminal window
3. Starts frontend in new terminal window

Usage:
```bat
runapplication.bat
```

## Local Development Quick Start

1. Setup everything:
```bat
setupdev.bat
```

2. Launch app:
```bat
runapplication.bat
```

3. Open:
- Frontend: `http://127.0.0.1:5173`
- Backend docs: `http://127.0.0.1:8000/docs`

## Testing

Run backend tests:

```bat
python -m pytest -q
```

Current test coverage includes:
- create pet
- get pets
- adopt pet
- re-adoption failure (`400`)
- invalid ID (`404`)

## Notes

- `main.py` intentionally does **not** call `Base.metadata.create_all(...)`; schema is migration-managed.
- CORS is enabled for frontend dev origins (`localhost:5173`, `127.0.0.1:5173`).
- For reproducible environments, keep using `setupdev.bat` and Alembic migrations.
