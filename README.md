# FurFinds
### Find. Adopt. Love.

FurFinds is a full-stack pet adoption platform built for the intern coding challenge requirements and extended with practical extras (analytics, recommendations, and realtime updates).  
The app is designed for local execution and evaluation after cloning.

---

## Intern Coding Challenge Mapping

This section directly answers the challenge checklist.

### 1) Backend Development (FastAPI + SQLite)
- Backend is implemented using `FastAPI`.
- Required endpoints are available:
  - `POST /pets/` (add pet)
  - `POST /pets/{id}/adopt` (adopt pet)
- OpenAPI standards are followed:
  - Swagger UI: `http://127.0.0.1:8000/docs`
  - OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
- Error handling included with proper HTTP responses:
  - invalid auth -> `401`
  - duplicate user -> `400`
  - adopt already adopted pet -> `400`
  - pet not found -> `404`
- Dependency injection is used for DB session and auth dependencies.
- Unit tests are included under `tests/`.

#### Trick Logic (Adoption Rule)
- Adoption is blocked if a pet is already adopted.
- Example behavior:
  - First adopt call for a pet -> success
  - Second adopt call for same pet -> rejected with error

### 2) Database (SQLite + Alembic)
- SQLite is used (`pets.db` at runtime, ignored in git).
- Alembic migrations are included in `alembic/versions/`.
- Base pets schema includes:
  - `id`, `name`, `type`, `adopted`
- Additional profile fields are added through migrations to match the Add Pet UI.
- `seed_data.sql` can be used for optional SQL-based seeding (or API/manual data entry).

### 3) Frontend (React + Axios)
- Frontend is built using React (Vite).
- Axios is used for all backend API calls.
- Frontend supports:
  - viewing pets
  - adopting pets
  - filtering/searching pets
- Frontend does not access DB directly.
- Bonus implemented:
  - realtime updates through WebSocket events
  - analytics charts

### 4) Python SDK (OpenAPI Generator)
- `pet_sdk/` is included as generated Python SDK output.
- SDK generation command:
```bash
npm install -g @openapitools/openapi-generator-cli
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o pet_sdk
```
- Example usage:
```python
from pet_sdk.api.pets_api import PetsApi
from pet_sdk import ApiClient

client = ApiClient()
api = PetsApi(client)
# result = api.<your_method_here>()
# print(result)
```

### 5) Setup Script (`setupdev.bat`)
- Setup automation is provided in `setupdev.bat`.
- It creates venv, installs backend/frontend dependencies, and runs migrations.

### 6) Run Script (`runapplication.bat`)
- Full application launcher is provided in `runapplication.bat`.
- It starts backend and frontend in separate terminal windows.

### Additional Notes from Challenge
- Docker is not required and not used.
- Validation and error handling are implemented.
- Frontend focuses on functionality over visual complexity.

---

## Features

- JWT-based auth (`/auth/register`, `/auth/login`)
- Role-based access (user/admin)
- Add pet / view pets / adopt pet flow
- Duplicate adoption prevention
- Pet filtering and search
- Analytics dashboard (adoption/type/city/vaccination/age)
- AI recommendation endpoint
- Realtime adoption event updates via WebSocket

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- PyJWT + bcrypt
- Pytest

### Frontend
- React (Vite)
- React Router
- Axios
- Chart.js (`react-chartjs-2`)

### SDK
- OpenAPI Generator CLI
- Generated Python SDK in `pet_sdk/`

---

## Project Structure

```text
FurFinds/
  main.py                      # FastAPI app entrypoint
  models.py                    # SQLAlchemy models
  schemas.py                   # Pydantic schemas
  crud.py                      # DB operations and business logic
  dependencies.py              # auth/db dependencies
  security.py                  # JWT + password hashing
  routers/                     # API route modules (pets, auth, admin, etc.)
  alembic/                     # migration config + versions
  tests/                       # backend tests
  frontend/                    # React frontend
  pet_sdk/                     # generated Python SDK
  setupdev.bat                 # setup automation
  runapplication.bat           # run automation
  openapi.json                 # OpenAPI spec snapshot
```

---

## Admin Credentials (Default)

- Email: `admin@furfinds.com`
- Password: `Admin@123`

### Why default admin exists
- Evaluators need immediate access to admin-only functionality without manual DB edits.
- Admin routes are restricted by role checks, so a normal registered user cannot act as admin.
- Normal users created through `/auth/register` are assigned role `user` by default.

---

## How to Run

### 1) Clone
```bash
git clone <repo_url>
cd FurFinds
```

### 2) Setup once
```bat
setupdev.bat
```

### 3) Run modes

#### Backend only
```bat
call .venv\Scripts\activate.bat
python -m uvicorn --app-dir . main:app --reload --host 127.0.0.1 --port 8000
```

#### Frontend only
```bat
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

#### Full application
```bat
runapplication.bat
```

### Access URLs
- Frontend: `http://127.0.0.1:5173`
- Swagger: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

---

## API Summary

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Pets
- `GET /pets/`
- `POST /pets/`
- `POST /pets/{id}/adopt`
- `POST /pets/recommend`

### Other
- `POST /recommend`
- `GET /analytics`
- `GET /admin/users` (admin only)
- `WS /ws`

---

## Testing

Run backend tests:
```bat
call .venv\Scripts\activate.bat
python -m pytest -q
```

---

## Evaluator Quick Verification

1. Run `setupdev.bat`
2. Run `runapplication.bat`
3. Open Swagger at `/docs` and verify required endpoints
4. Login as admin using default credentials
5. Add a pet (`POST /pets/`) and adopt a pet (`POST /pets/{id}/adopt`)
6. Try adopting same pet again -> should fail
7. Open frontend and verify pets list + adoption flow + charts

---

## Troubleshooting

- If backend dependencies are missing:
```bat
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
```
- If DB needs reset:
```bat
call .venv\Scripts\activate.bat
python -m alembic upgrade head
```
- If frontend dependencies are missing:
```bat
cd frontend
npm install
```
