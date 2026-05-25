from sqlalchemy.orm import Session

from backend.models import InventoryItem
from backend.services.waste_risk_engine import calculate_waste_risk, is_food_category, normalize


def build_summary(db: Session) -> dict:
    items = db.query(InventoryItem).all()
    predictions = [calculate_waste_risk(item) for item in items]

    high_risk = [p for p in predictions if p.risk_score >= 61]
    estimated_waste_value = round(sum(p.estimated_loss for p in predictions), 2)
    suggested_donation_quantity = round(
        sum(p.predicted_waste_quantity for item, p in zip(items, predictions) if is_food_category(item.category) and p.risk_score >= 61),
        2,
    )
    plastic_waste_avoided = round(
        sum(p.predicted_waste_quantity for item, p in zip(items, predictions) if "plastic" in normalize(item.category)),
        2,
    )
    estimated_food_saved = round(suggested_donation_quantity * 0.85, 2)

    return {
        "total_products_monitored": len(items),
        "high_risk_products": len(high_risk),
        "estimated_waste_value": estimated_waste_value,
        "estimated_food_saved": estimated_food_saved,
        "suggested_donation_quantity": suggested_donation_quantity,
        "plastic_waste_avoided": plastic_waste_avoided,
        "critical_alerts": [p.product_name for p in predictions if p.risk_level == "Critical"],
    }

