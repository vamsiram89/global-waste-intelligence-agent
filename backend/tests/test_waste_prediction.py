import os
from datetime import date, timedelta
from types import SimpleNamespace

os.environ["DATABASE_URL"] = "sqlite:///./test_waste_intelligence.db"

from fastapi.testclient import TestClient

from backend.database import Base, SessionLocal, engine
from backend.main import app
from backend.models import InventoryItem, NGO
from backend.services.ngo_matcher import find_best_ngo
from backend.services.recommendation_engine import build_recommendation
from backend.services.waste_risk_engine import calculate_waste_risk


def item(**overrides):
    base = {
        "product_name": "Test Item",
        "category": "Dairy",
        "quantity": 40,
        "expiry_date": date.today() + timedelta(days=10),
        "avg_daily_sales": 20,
        "cost_per_unit": 1.0,
        "storage_condition": "cold",
        "demand_level": "high",
        "weather_factor": "normal",
        "event_factor": "festival",
    }
    base.update(overrides)
    return SimpleNamespace(**base)


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_low_risk_item():
    risk = calculate_waste_risk(item())
    assert risk.risk_level == "Low"
    assert risk.risk_score <= 30


def test_medium_risk_item():
    risk = calculate_waste_risk(
        item(quantity=250, expiry_date=date.today() + timedelta(days=8), avg_daily_sales=20, demand_level="medium", event_factor="none")
    )
    assert risk.risk_level == "Medium"


def test_high_risk_item():
    risk = calculate_waste_risk(
        item(quantity=80, expiry_date=date.today() + timedelta(days=3), avg_daily_sales=18, demand_level="low", weather_factor="hot", event_factor="none")
    )
    assert risk.risk_level == "High"


def test_critical_risk_item():
    risk = calculate_waste_risk(
        item(quantity=220, expiry_date=date.today() + timedelta(days=1), avg_daily_sales=8, demand_level="low", weather_factor="hot", event_factor="negative")
    )
    assert risk.risk_level == "Critical"


def test_expired_item_should_not_be_donated():
    expired = InventoryItem(
        product_name="Expired Meals",
        category="Restaurant Meals",
        quantity=20,
        unit="meals",
        expiry_date=date.today() - timedelta(days=1),
        purchase_date=date.today() - timedelta(days=3),
        avg_daily_sales=1,
        cost_per_unit=2.0,
        storage_condition="cold",
        demand_level="low",
        weather_factor="normal",
        event_factor="none",
    )
    risk = calculate_waste_risk(expired)
    action_type, message, urgency = build_recommendation(expired, risk)
    assert action_type == "safe_disposal"
    assert "Do not donate" in message
    assert urgency == "critical"


def test_ngo_matching_works():
    reset_db()
    db = SessionLocal()
    try:
        inventory = InventoryItem(
            product_name="Safe Bakery Bread",
            category="Bakery",
            quantity=50,
            unit="loaves",
            expiry_date=date.today() + timedelta(days=2),
            purchase_date=date.today(),
            avg_daily_sales=5,
            cost_per_unit=1.0,
            storage_condition="ambient",
            demand_level="low",
            weather_factor="normal",
            event_factor="none",
        )
        ngo = NGO(name="Food Bank", location="Central City", accepted_categories="all_food,bakery", capacity=100, contact="food@example.org")
        db.add_all([inventory, ngo])
        db.commit()
        matched = find_best_ngo(db, inventory, 25)
        assert matched is not None
        assert matched.name == "Food Bank"
    finally:
        db.close()


def test_recommendation_generated_correctly():
    risky = InventoryItem(
        product_name="Unsold Meals",
        category="Restaurant Meals",
        quantity=90,
        unit="meals",
        expiry_date=date.today() + timedelta(days=1),
        purchase_date=date.today(),
        avg_daily_sales=8,
        cost_per_unit=2.5,
        storage_condition="cold",
        demand_level="low",
        weather_factor="storm",
        event_factor="cancellation",
    )
    risk = calculate_waste_risk(risky)
    action_type, message, urgency = build_recommendation(risky, risk)
    assert action_type == "urgent_discount_and_redistribution"
    assert "NGO redistribution" in message
    assert urgency == "critical"


def test_api_health_and_prediction_endpoint():
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    payload = {
        "product_name": "API Yogurt",
        "category": "Dairy",
        "quantity": 100,
        "unit": "cups",
        "expiry_date": (date.today() + timedelta(days=2)).isoformat(),
        "purchase_date": date.today().isoformat(),
        "avg_daily_sales": 10,
        "cost_per_unit": 0.8,
        "storage_condition": "cold",
        "demand_level": "low",
        "weather_factor": "hot",
        "event_factor": "none",
    }
    response = client.post("/predict/waste-risk", json=payload)
    assert response.status_code == 200
    assert response.json()["risk_level"] in {"High", "Critical"}
