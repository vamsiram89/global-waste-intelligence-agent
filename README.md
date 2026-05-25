# Global Waste Intelligence Agent

**AI that reduces waste before it is produced**

Global Waste Intelligence Agent is a realistic MVP for predicting food, inventory, packaging, and overproduction waste before it becomes garbage. It combines FastAPI, SQLite, explainable risk scoring, lightweight ML-style normalization, NGO matching, and a Streamlit dashboard for a portfolio, startup demo, or interview walkthrough.

## Features

- Inventory waste prediction for grocery, restaurant, warehouse, home, and factory items
- Explainable 0-100 waste risk score with Low, Medium, High, and Critical levels
- Smart discount and clearance recommendations
- Food redistribution suggestions to nearby NGOs, shelters, food banks, orphanages, and community kitchens
- Overproduction prevention guidance for restaurants and factories
- Analytics for predicted loss, food saved, plastic avoided, and high-risk inventory
- Safety rules to prevent donation recommendations for expired food
- Audit logs for important prediction, recommendation, and redistribution decisions

## Architecture

```text
Streamlit Dashboard
        |
        | HTTP API
        v
FastAPI Backend
        |
        | SQLAlchemy ORM
        v
SQLite MVP Database
        |
        v
Risk Engine + Recommendation Engine + NGO Matcher + Analytics Service
```

## Tech Stack

- Backend: Python, FastAPI, Pydantic, SQLAlchemy, SQLite
- AI logic: rule-based scoring, Pandas/NumPy helpers, scikit-learn-compatible structure
- Frontend: Streamlit
- Testing: Pytest, FastAPI TestClient
- Packaging: Docker, Docker Compose

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Copy environment variables.

```powershell
Copy-Item .env.example .env
```

4. Seed the database.

```powershell
python -m backend.seed_data
```

## Run Backend

```powershell
uvicorn backend.main:app --reload --port 8000
```

Backend docs:

- Swagger UI: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health>

## Run Frontend

In a second terminal:

```powershell
streamlit run frontend/streamlit_app.py
```

Set `API_BASE_URL` if the backend is not running on `http://localhost:8000`.

## API Endpoints

- `POST /inventory/add` - Add inventory item
- `GET /inventory` - List inventory items
- `POST /predict/waste-risk` - Predict waste risk for one item payload
- `GET /predict/all` - Predict waste risk for all stored inventory
- `POST /actions/recommend` - Generate action recommendation for an item
- `GET /ngos` - List sample NGO and food redistribution partners
- `POST /redistribute` - Match excess safe food to an NGO
- `GET /analytics/summary` - Get portfolio-ready waste prevention summary

## API Examples

Add inventory:

```bash
curl -X POST http://localhost:8000/inventory/add \
  -H "Content-Type: application/json" \
  -d '{"product_name":"Yogurt Cups","category":"Dairy","quantity":120,"unit":"cups","expiry_date":"2026-05-27","purchase_date":"2026-05-20","avg_daily_sales":18,"cost_per_unit":0.8,"storage_condition":"cold","demand_level":"low","weather_factor":"hot","event_factor":"none"}'
```

Predict all:

```bash
curl http://localhost:8000/predict/all
```

## Demo Flow

1. Seed the database with `python -m backend.seed_data`.
2. Open the Streamlit dashboard.
3. Visit **Demo Scenarios** and load examples like supermarket yogurt expiry or restaurant unsold meals.
4. Go to **Waste Prediction** to inspect risk scores and reasons.
5. Go to **Action Recommendations** to generate discount, donation, order reduction, or recycling actions.
6. Go to **NGO Matching** to match safe surplus food before expiry.
7. Review analytics for estimated money saved, food saved, and plastic avoided.

## Safety Disclaimer

This MVP is a decision-support prototype. Real deployment must include food safety validation, local legal compliance, cold-chain checks, expiry verification, partner approval, and human confirmation before any redistribution or pickup is scheduled.

## Future Enhancements

- POS and ERP integrations
- Real weather and local event APIs
- Production forecasting with historical sales model training
- Route optimization for donations
- Packaging supplier scorecards
- Multi-tenant authentication and role-based access
- Human approval workflow and compliance audit exports

