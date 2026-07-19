# CarePilot AI

CarePilot AI is an AI-powered healthcare assistant designed for a hackathon demo. It combines a React frontend with a FastAPI backend to provide a polished experience for symptom analysis, medical report review, and historical insight tracking.

## Features

- User registration and login
- JWT-based authentication
- Protected routes
- Symptom analysis with explanation and recommendations
- Medical report review with summary and risk insights
- Analysis history and account overview
- Responsive healthcare-style dashboard

## Tech stack

- Frontend: React, Vite, React Router, Axios, Bootstrap
- Backend: FastAPI, SQLAlchemy, Pydantic, JWT
- Database: SQLite

## Run locally

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open:

- Frontend: http://localhost:5173/
- Backend API: http://127.0.0.1:8000/

> If PowerShell blocks `npm.ps1` on your machine, use `npm.cmd install` and
> `npm.cmd run dev` instead.

## Demo flow

1. Register or log in.
2. Open the dashboard.
3. Enter symptoms and review the AI analysis.
4. Paste or review a medical report summary.
5. Review your analysis history.

## Project goals

CarePilot AI demonstrates how AI-assisted health guidance can be presented in a simple, approachable, and demo-friendly experience for early-stage healthcare support.
