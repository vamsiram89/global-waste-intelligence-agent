from datetime import date

from sqlalchemy.orm import Session

from backend.models import InventoryItem, NGO
from backend.services.waste_risk_engine import is_food_category, normalize


def ngo_accepts(ngo: NGO, category: str) -> bool:
    accepted = [normalize(part) for part in ngo.accepted_categories.split(",")]
    normalized_category = normalize(category)
    return "all_food" in accepted or normalized_category in accepted


def find_best_ngo(db: Session, item: InventoryItem, quantity: float) -> NGO | None:
    if item.expiry_date < date.today() or not is_food_category(item.category):
        return None

    candidates = db.query(NGO).all()
    valid = [ngo for ngo in candidates if ngo.capacity >= quantity and ngo_accepts(ngo, item.category)]
    if not valid:
        return None

    same_location = [ngo for ngo in valid if normalize(ngo.location) == normalize("Central City")]
    return (same_location or valid)[0]

