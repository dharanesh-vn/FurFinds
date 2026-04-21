# FurFinds Frontend

## Overview

FurFinds frontend is a React (Vite) client for the pet adoption system.  
It consumes only backend APIs through Axios and provides complete UI flows for authentication, pet exploration, adoption, analytics, recommendations, and admin control.

## What This Frontend Delivers

- Secure login/register flow with protected routes
- Dashboard with quick metrics and personalized greeting
- Rich pet discovery with search + multi-filter controls
- Card-based pet listing and adopt action
- AI recommendation page with explanation output
- Analytics charts for adoption and distribution insights
- Admin dashboard with table-based pet management
- Real-time UI updates through backend WebSocket adoption events

## Admin Access (Pre-Seeded)

- Email: [admin@furfinds.com](mailto:admin@furfinds.com)
- Password: `Admin@123`

Use this account to access admin-only UI routes.

## Run Methods

### Method 1: Scripts (Recommended)

From repository root:

```bash
setupdev.bat
runapplication.bat
```

What scripts do from a frontend perspective:

- Ensure frontend dependencies are installed (`npm install`)
- Start frontend dev server (`npm run dev`) in a dedicated terminal window
- Coordinate with backend startup for full-stack launch

### Method 2: Manual Backend + Frontend Run

Backend (required for API access):

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

For already prepared environments:

```bash
cd backend
uvicorn main:app --reload
```

```bash
cd frontend
npm run dev
```

### Method 4: SDK Regeneration/Usage (Optional)

The frontend does not consume `pet_sdk`, but SDK generation is documented for assignment completeness:

```bash
npm install -g @openapitools/openapi-generator-cli
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o pet_sdk
```

## Page Structure And UI Flow

- `/` - Landing page
- `/login` - User login
- `/register` - User registration
- `/dashboard` - Personalized summary and quick links
- `/pets` - Pet list, filters, search, adopt
- `/add-pet` - Pet creation form
- `/analytics` - Chart-based adoption insights
- `/ai-recommendation` - Preference input and recommended pets
- `/admin` - Admin panel (role-guarded)

Typical flow:

1. Login
2. Dashboard (`Welcome, <username>`)
3. Navigate to Pets / Add Pet / Analytics / AI Recommendation
4. Admin users can access Admin dashboard

## Filter System

The pets page supports layered filtering and search:

- Type
- Breed
- Age
- Gender
- Vaccinated
- Sterilized
- City
- Status (All/Available/Adopted)
- Text search (name/type/breed/city)

Filters can be combined and cleared quickly.

## AI Recommendation UI

- Takes free-text preferences (for example: apartment, city, low maintenance)
- Calls recommendation endpoint
- Displays recommended pets and reason/explanation in styled output cards

## Admin UI

- Distinct dashboard-style page
- Summary stats: total/adopted/available
- User list visibility
- Pet management table (edit/delete actions)
- Status column for adopted/available tracking

## Unique Features Reflected In UI

- Supports realistic 200-pet Tamil Nadu dataset
- Real-time updates for adoption changes
- Analytics and recommendation capabilities beyond basic CRUD
- Unified modern layout and navigation consistency across pages

## Error Handling And Edge Cases

- API errors are rendered safely (no hard crashes)
- Validation issues are shown to users in context
- Unauthorized access is routed through protected-route logic
- Duplicate adoption rejection is surfaced through backend response messaging

## Build / Quality Check

```bash
cd frontend
npm run build
```

## Assignment Alignment

- React frontend implemented and API-only integration enforced
- Axios used for all HTTP communication
- View and adopt workflows implemented
- Works with FastAPI/SQLite backend and OpenAPI schema
- Includes bonus-level UX features (analytics, AI recommendation, realtime, admin UX)
