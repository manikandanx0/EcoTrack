# EcoTrack

Hybrid carbon footprint tracker with a FastAPI backend and React frontend. Calculate a baseline footprint, get AI-assisted refinements, and view offset suggestions.

## Quick start

Prereqs: Python 3.8+, Node 16+, npm

1) Backend
```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
API: http://localhost:8000
Docs: http://localhost:8000/docs

2) Frontend
```
cd frontend
npm install
npm run dev
```
App: http://localhost:5173

Optional (ML model):
```
cd ml
python train_model.py
```

## How it works
- Input transport, food, energy, waste, and consumption.
- Backend computes a baseline using emission factors in `shared/conversion_factors.json`.
- Optional ML step refines energy usage if extra fields are provided.

## Common commands
```
# Backend
uvicorn main:app --reload --port 8000

# Frontend
npm run dev
```

## API (auth required unless noted)
- POST `/auth/register` (no auth)
- POST `/auth/login` (no auth)
- GET `/auth/me`
- POST `/api/calc`
- POST `/api/refine`
- POST `/api/offset`
- GET `/api/leaderboard` (no auth)
- POST `/api/suggest`

## Troubleshooting
- 422 on `/api/calc`: ensure Authorization header is set and body matches `InputPayload`.
- 500 on `/api/calc`: check server logs; invalid response types in `details` were fixed to allow strings.
- Frontend blank screen: hard refresh; check browser console for errors.

## Tech stack
- Backend: FastAPI, SQLAlchemy, Pydantic
- Frontend: React, Vite, Tailwind, Recharts
- ML: scikit-learn (optional)

## License
MIT


Thank you