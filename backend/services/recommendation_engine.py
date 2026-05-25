from datetime import date

from backend.models import InventoryItem
from backend.services.waste_risk_engine import RiskResult, is_food_category, normalize


def build_recommendation(item: InventoryItem, risk: RiskResult) -> tuple[str, str, str]:
    expired = item.expiry_date < date.today()
    food = is_food_category(item.category)
    category = normalize(item.category)

    if expired:
        return (
            "safe_disposal",
            "Do not donate. Item is expired; follow food safety disposal or approved recycling procedures.",
            "critical",
        )

    if risk.risk_score >= 81:
        if food:
            return (
                "urgent_discount_and_redistribution",
                "Apply urgent clearance pricing and request human-approved NGO redistribution before expiry.",
                "critical",
            )
        return (
            "urgent_clearance_and_recycling",
            "Run urgent clearance, reduce next supplier order, and prepare packaging recycling plan.",
            "critical",
        )

    if risk.risk_score >= 61:
        if food:
            return (
                "25_percent_discount",
                "Apply a 25% discount today and prepare donation if sell-through does not improve.",
                "high",
            )
        return (
            "reduce_next_order",
            "Reduce next order or production batch and move excess stock to bundled promotions.",
            "high",
        )

    if risk.risk_score >= 31:
        if "plastic" in category:
            return (
                "supplier_order_reduction",
                "Reduce next supplier order and track plastic packaging avoided.",
                "medium",
            )
        return (
            "10_percent_discount",
            "Apply a 10% demand-stimulation discount and monitor sales velocity.",
            "medium",
        )

    return (
        "monitor",
        "Risk is low. Continue monitoring inventory and sales velocity.",
        "low",
    )


def overproduction_advice(item: InventoryItem, risk: RiskResult) -> str | None:
    factory_or_restaurant = normalize(item.category) in {"prepared_food", "restaurant_meals", "beverage"}
    if not factory_or_restaurant:
        return None
    if risk.risk_score >= 61 or normalize(item.demand_level) == "low":
        return "Reduce the next production batch by 15-30% until demand recovers."
    return "Production level looks acceptable; keep monitoring sell-through."

