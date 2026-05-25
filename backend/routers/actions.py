from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import AuditLog, InventoryItem, RecommendedAction
from backend.schemas import ActionRequest, RecommendedActionRead
from backend.services.recommendation_engine import build_recommendation, overproduction_advice
from backend.services.waste_risk_engine import calculate_waste_risk

router = APIRouter(prefix="/actions", tags=["actions"])


@router.post("/recommend", response_model=RecommendedActionRead)
def recommend_action(payload: ActionRequest, db: Session = Depends(get_db)) -> RecommendedActionRead:
    item = db.get(InventoryItem, payload.inventory_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    risk = calculate_waste_risk(item)
    action_type, message, urgency = build_recommendation(item, risk)
    production_note = overproduction_advice(item, risk)
    if production_note:
        message = f"{message} Overproduction prevention: {production_note}"

    action = RecommendedAction(
        inventory_item_id=item.id,
        action_type=action_type,
        action_message=message,
        urgency=urgency,
    )
    db.add(action)
    db.add(AuditLog(event_type="action_recommended", message=f"Recommended {action_type} for {item.product_name}."))
    db.commit()
    db.refresh(action)

    return RecommendedActionRead(
        id=action.id,
        inventory_item_id=item.id,
        product_name=item.product_name,
        action_type=action.action_type,
        action_message=action.action_message,
        urgency=action.urgency,
        created_at=action.created_at,
    )

