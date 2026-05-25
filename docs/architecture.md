# Architecture

## System Architecture

```text
User
 |
 v
Streamlit Dashboard
 |
 v
FastAPI API Layer
 |
 +--> Inventory Router
 +--> Prediction Router
 +--> Actions Router
 +--> NGO Router
 +--> Analytics Router
 |
 v
SQLAlchemy Services
 |
 v
SQLite Database
```

## Agent Workflow

1. A user adds an inventory or production item.
2. The waste risk engine calculates days until expiry, demand coverage, overstock risk, weather impact, event impact, and storage condition risk.
3. The recommendation engine translates the score into discount, donation, production reduction, conversion, or recycling actions.
4. The NGO matcher filters partners by category, capacity, location, and food safety rules.
5. The dashboard displays metrics and explainable decisions.

## Data Flow

```text
Inventory Item
  -> Waste Risk Engine
  -> Waste Prediction Record
  -> Recommendation Engine
  -> Recommended Action Record
  -> Analytics Summary
```

## AI Risk Scoring

The MVP uses an explainable hybrid approach:

- Rule-based scoring for expiry, overstock, demand, weather, events, and storage conditions
- Lightweight numerical normalization using Python data structures that can later be replaced by trained models
- Category-aware adjustments for dairy, bakery, cooked meals, plastic-packaged products, and shelf-stable inventory

Risk levels:

- `0-30`: Low
- `31-60`: Medium
- `61-80`: High
- `81-100`: Critical

## Safety Rules

- Expired food is never recommended for donation.
- Donation is only suggested when the item is food, not expired, and an NGO accepts the category.
- Redistribution requests are created with `pending_human_approval` status.
- Audit logs capture prediction, recommendation, and redistribution decisions.

