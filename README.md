# FurFinds - Find. Adopt. Love.

FurFinds is a production-style full-stack pet adoption platform that demonstrates clean API design, migration-driven database management, real-time updates, generated SDK integration, and practical AI/RAG features.

It is designed as a portfolio-ready engineering project: clear architecture, test coverage, and recruiter-friendly implementation choices.

## Project Overview

FurFinds enables users to:
- Add pets to the adoption platform
- Browse available pets
- Adopt pets with business-rule validation
- Receive real-time adoption updates via WebSockets
- Get AI-powered pet recommendations based on natural language preferences
- Track adoption analytics in the frontend dashboard

## Tech Stack

- Backend: FastAPI, SQLAlchemy, SQLite, Alembic, Pytest
- Frontend: React (Vite), Axios, Chart.js (`react-chartjs-2`)
- AI/RAG: ChromaDB vector store + LLM-generated explanation (OpenAI-compatible API)
- SDK: OpenAPI Generator CLI (Python client)
- Automation: `setupdev.bat`, `runapplication.bat`

## Architecture Overview

FurFinds follows a layered architecture:

- API Layer (`routers/`): HTTP/WebSocket endpoints and request validation
- Domain/Data Access Layer (`crud.py`): persistence and business logic
- Data Layer (`models.py`, `database.py`, Alembic): schema + DB sessions + migrations
- AI Layer (`ai_recommender.py`): vector retrieval + LLM reasoning for recommendations
- Client Layer (`frontend/`): interactive UI with REST + WebSocket integration
- Integration Layer (`pet_sdk/`): generated Python SDK from OpenAPI schema

### High-Level Flow

1. Frontend calls FastAPI endpoints (`/pets`, `/recommend`, `/analytics`)
2. Backend executes CRUD through SQLAlchemy sessions
3. On adoption, backend broadcasts event to `/ws` clients
4. Recommendation requests are processed via ChromaDB retrieval and LLM explanation generation
5. Frontend updates state in real time and visualizes analytics

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js + npm
- Windows environment (batch scripts provided)

### Option A: One-command setup (recommended)

```bat
setupdev.bat
```

What it does:
1. Creates `.venv`
2. Installs backend dependencies
3. Runs `alembic upgrade head`
4. Installs frontend dependencies

### Run the full application

```bat
runapplication.bat
```

Starts:
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`

### Manual startup (optional)

Backend:
```bat
call .venv\Scripts\activate.bat
python -m uvicorn main:app --reload
```

Frontend:
```bat
cd frontend
npm run dev
```

### Frontend environment configuration

Backend URLs are configurable from `frontend/.env` (see `frontend/.env.example`):

- `VITE_API_BASE_URL` (default: `http://127.0.0.1:8000`)
- `VITE_WS_BASE_URL` (optional, auto-derived from API URL if omitted)

## API Documentation

Base URL: `http://127.0.0.1:8000`  
Interactive docs: `http://127.0.0.1:8000/docs`

### Core Pet Endpoints

- `POST /pets/` - create a pet
- `GET /pets/` - list pets
- `POST /pets/{id}/adopt` - adopt a pet
  - `400` if already adopted
  - `404` if pet not found

### AI Recommendation Endpoints

- `POST /recommend`
  - Input:
    ```json
    { "preference_text": "small pet for apartment", "top_k": 3 }
    ```
  - Output:
    ```json
    {
      "recommendations": [{ "id": 1, "name": "Coco", "type": "Rabbit", "adopted": false }],
      "explanation": "..."
    }
    ```

- `POST /pets/recommend` (compatible variant used by existing frontend flow)

### Analytics Endpoint

- `GET /analytics`
  - Output:
    ```json
    { "total_pets": 10, "adopted_count": 4, "adoption_rate": 0.4 }
    ```

### Real-Time Endpoint

- `WS /ws`
  - Broadcast event on adoption:
    ```json
    {
      "event": "pet_adopted",
      "pet": { "id": 5, "name": "Luna", "type": "Cat", "adopted": true }
    }
    ```

## SDK Usage (Python)

The generated Python SDK lives in `pet_sdk/`.

### Run example script

```bat
python pet_sdk/example_usage.py
```

The example demonstrates:
- listing pets
- creating a pet when needed
- adopting a pet

### Regenerate SDK (if API changes)

1. Export OpenAPI schema:
```bat
python -c "import json; from main import app; open('openapi.json','w',encoding='utf-8').write(json.dumps(app.openapi(), indent=2))"
```

2. Generate SDK:
```bat
npx @openapitools/openapi-generator-cli generate -i openapi.json -g python -o pet_sdk
```

## AI Feature Explanation (RAG)

FurFinds includes a lightweight retrieval-augmented recommendation pipeline:

1. User submits natural language preference text (for example: "small pet for apartment")
2. Backend creates/uses vector embeddings for available pets
3. ChromaDB retrieves the most relevant pets (`top_k`)
4. Backend generates a plain-language explanation using an LLM
5. If no LLM credentials are configured, the system returns a deterministic fallback explanation

### Optional LLM configuration

Set environment variables to enable generated explanations:
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional, default is set in code)
- `OPENAI_API_URL` (optional, OpenAI-compatible endpoint)

### Optional CORS configuration

For local development, FurFinds accepts `localhost` and `127.0.0.1` origins across ports.
If you need to override explicitly, set:

- `CORS_ORIGINS` as comma-separated origins (example: `http://localhost:5173,http://127.0.0.1:5173`)

## Testing

Run backend tests:

```bat
python -m pytest -q
```

Coverage includes:
- pet CRUD behavior
- adoption business rules
- recommendation endpoints
- analytics endpoint

## Recruiter Notes

This project demonstrates:
- Full-stack product thinking (API + frontend + UX)
- Production-minded backend practices (migrations, validation, tests)
- AI integration beyond prompt-only usage (retrieval + reasoning)
- Real-time systems integration with WebSockets
- Developer experience tooling (automation scripts, generated SDK, docs)
