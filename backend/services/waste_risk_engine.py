from dataclasses import dataclass
from datetime import date
from math import ceil
from typing import Protocol

try:
    import numpy as np
    from sklearn.ensemble import IsolationForest
except ModuleNotFoundError:
    np = None
    IsolationForest = None


class InventoryLike(Protocol):
    product_name: str
    category: str
    quantity: float
    expiry_date: date
    avg_daily_sales: float
    cost_per_unit: float
    storage_condition: str
    demand_level: str
    weather_factor: str
    event_factor: str


@dataclass
class RiskResult:
    product_name: str
    category: str
    risk_score: float
    risk_level: str
    predicted_waste_quantity: float
    estimated_loss: float
    reason: str
    days_until_expiry: int


FOOD_CATEGORIES = {
    "dairy",
    "fruit",
    "produce",
    "prepared_food",
    "restaurant_meals",
    "bakery",
    "beverage",
    "vegetables",
}

PERISHABLE_CATEGORIES = FOOD_CATEGORIES | {"meat", "seafood"}


def normalize(value: str | None) -> str:
    return (value or "").strip().lower().replace(" ", "_")


def risk_level(score: float) -> str:
    if score <= 30:
        return "Low"
    if score <= 60:
        return "Medium"
    if score <= 80:
        return "High"
    return "Critical"


def is_food_category(category: str) -> bool:
    normalized = normalize(category)
    return normalized in FOOD_CATEGORIES or any(word in normalized for word in ["food", "meal", "dairy", "fruit"])


def lightweight_anomaly_adjustment(quantity: float, daily_sales: float, days_until_expiry: int) -> float:
    """Optional scikit-learn adjustment for unusual overstock patterns."""
    if np is None or IsolationForest is None:
        return 0.0

    baseline = np.array(
        [
            [20, 20, 10],
            [50, 25, 8],
            [80, 30, 7],
            [120, 35, 6],
            [200, 40, 5],
            [300, 45, 4],
        ]
    )
    model = IsolationForest(random_state=42, contamination=0.15)
    model.fit(baseline)
    prediction = model.predict([[quantity, daily_sales, max(days_until_expiry, 0)]])[0]
    return 5.0 if prediction == -1 else 0.0


def calculate_waste_risk(item: InventoryLike, today: date | None = None) -> RiskResult:
    today = today or date.today()
    days_until_expiry = (item.expiry_date - today).days
    daily_sales = max(item.avg_daily_sales, 0.1)
    days_to_sell_out = item.quantity / daily_sales
    excess_days = max(days_to_sell_out - max(days_until_expiry, 0), 0)

    score = 0.0
    reasons: list[str] = []

    if days_until_expiry < 0:
        score += 95
        reasons.append("Item is already expired and must not be donated.")
    elif days_until_expiry <= 1:
        score += 45
        reasons.append("Expiry is within 1 day.")
    elif days_until_expiry <= 3:
        score += 34
        reasons.append("Expiry is within 3 days.")
    elif days_until_expiry <= 7:
        score += 20
        reasons.append("Expiry is within 7 days.")
    else:
        score += 6
        reasons.append("Expiry window is not immediate.")

    coverage_ratio = days_to_sell_out / max(days_until_expiry, 1)
    if coverage_ratio >= 3:
        score += 28
        reasons.append("Stock coverage is far above expected sell-through.")
    elif coverage_ratio >= 1.5:
        score += 18
        reasons.append("Stock may not sell before expiry.")
    elif coverage_ratio >= 1:
        score += 10
        reasons.append("Stock sell-through is close to expiry deadline.")
    else:
        score += 2
        reasons.append("Sales velocity can likely clear stock.")

    demand = normalize(item.demand_level)
    if demand == "low":
        score += 15
        reasons.append("Demand level is low.")
    elif demand == "medium":
        score += 7
        reasons.append("Demand is moderate.")
    elif demand == "high":
        score -= 6
        reasons.append("High demand reduces risk.")

    weather = normalize(item.weather_factor)
    if weather in {"hot", "heatwave", "humid"} and normalize(item.category) in PERISHABLE_CATEGORIES:
        score += 10
        reasons.append("Weather can accelerate spoilage.")
    elif weather in {"storm", "rain"}:
        score += 6
        reasons.append("Weather may reduce customer visits.")

    event = normalize(item.event_factor)
    if event in {"negative", "low_footfall", "road_closure", "cancellation"}:
        score += 10
        reasons.append("Local event impact reduces demand.")
    elif event in {"festival", "sports", "market_day", "positive"}:
        score -= 8
        reasons.append("Positive local event may increase demand.")

    storage = normalize(item.storage_condition)
    if storage in {"poor", "warm", "damaged"}:
        score += 12
        reasons.append("Storage condition increases waste risk.")
    elif storage in {"cold", "frozen", "controlled"}:
        score -= 4
        reasons.append("Good storage reduces spoilage risk.")

    category = normalize(item.category)
    if category in {"dairy", "prepared_food", "restaurant_meals", "bakery"}:
        score += 8
        reasons.append("Category is highly perishable.")
    elif "plastic" in category and coverage_ratio >= 2:
        score += 7
        reasons.append("Plastic-packaged overstock creates packaging waste risk.")

    anomaly_adjustment = lightweight_anomaly_adjustment(item.quantity, daily_sales, days_until_expiry)
    if anomaly_adjustment:
        score += anomaly_adjustment
        reasons.append("Lightweight anomaly check detected unusual stock pressure.")

    score = round(max(0, min(score, 100)), 2)
    predicted_quantity = min(item.quantity, max(excess_days * daily_sales, 0))
    if score >= 81:
        predicted_quantity = max(predicted_quantity, item.quantity * 0.55)
    elif score >= 61:
        predicted_quantity = max(predicted_quantity, item.quantity * 0.35)
    elif score >= 31:
        predicted_quantity = max(predicted_quantity, item.quantity * 0.15)
    else:
        predicted_quantity = max(predicted_quantity, item.quantity * 0.03)

    predicted_quantity = round(min(item.quantity, predicted_quantity), 2)
    estimated_loss = round(predicted_quantity * item.cost_per_unit, 2)
    reason = " ".join(reasons)

    return RiskResult(
        product_name=item.product_name,
        category=item.category,
        risk_score=score,
        risk_level=risk_level(score),
        predicted_waste_quantity=predicted_quantity,
        estimated_loss=estimated_loss,
        reason=reason,
        days_until_expiry=ceil(days_until_expiry),
    )
