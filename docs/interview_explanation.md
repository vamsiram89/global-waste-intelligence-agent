# Interview Explanation

## 30-Second Explanation

Global Waste Intelligence Agent is an AI-powered MVP that predicts waste before it happens. It analyzes inventory, expiry dates, sales velocity, demand, weather, events, and storage conditions to score waste risk, then recommends discounts, donations, order reductions, or recycling actions.

## 2-Minute Explanation

Most waste systems react after products are already discarded. This project flips the workflow by predicting risk while the product is still usable. A store, restaurant, warehouse, or factory adds inventory data through a FastAPI backend and Streamlit dashboard. The risk engine calculates expiry pressure, overstock, demand weakness, weather impact, and event impact. The recommendation engine turns that into practical actions, like urgent clearance, Buy 1 Get 1, donation before expiry, or reducing the next production batch. The NGO matcher suggests safe redistribution partners, while the analytics dashboard estimates money saved, food saved, and plastic avoided.

## Technical Explanation

The backend uses FastAPI, Pydantic, SQLAlchemy, and SQLite. The core AI logic is an explainable hybrid risk engine with lightweight numerical scoring that can later be replaced by trained forecasting models. The data model includes users, inventory items, waste predictions, recommended actions, NGOs, redistribution requests, and audit logs. Tests validate low, medium, high, critical, expired-food safety, NGO matching, and recommendation generation.

## Business Impact

The product helps reduce spoilage, overproduction, food insecurity, and packaging waste. It can sell as SaaS to stores and restaurants, enterprise software for factories, and a coordination platform for NGOs and governments.

## Resume Bullet Points

- Built an AI waste prevention MVP using FastAPI, SQLite, SQLAlchemy, Streamlit, and explainable risk scoring.
- Designed waste prediction logic using expiry pressure, demand velocity, overstock coverage, weather, events, storage, and category risk.
- Implemented recommendation workflows for discounts, redistribution, production reduction, conversion, and packaging recycling.
- Added safety guardrails to prevent expired food donation and require human approval for redistribution.
- Created tests, Docker setup, sample data, and interview-ready documentation.

