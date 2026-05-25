from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import AuditLog, InventoryItem, WastePrediction
from backend.schemas import InventoryItemCreate, WastePredictionRead
from backend.services.waste_risk_engine import calculate_waste_risk

router = APIRouter(prefix="/predict", tags=["prediction"])


@router.post("/waste-risk", response_model=WastePredictionRead)
def predict_single_item(payload: InventoryItemCreate) -> WastePredictionRead:
    risk = calculate_waste_risk(payload)
    return WastePredictionRead(**risk.__dict__)


@router.get("/all", response_model=list[WastePredictionRead])
def predict_all_inventory(db: Session = Depends(get_db)) -> list[WastePredictionRead]:
    responses: list[WastePredictionRead] = []
    for item in db.query(InventoryItem).all():
        risk = calculate_waste_risk(item)
        prediction = WastePrediction(
            inventory_item_id=item.id,
            risk_score=risk.risk_score,
            risk_level=risk.risk_level,
            predicted_waste_quantity=risk.predicted_waste_quantity,
            estimated_loss=risk.estimated_loss,
            reason=risk.reason,
        )
        db.add(prediction)
        db.add(AuditLog(event_type="prediction_created", message=f"Predicted {risk.risk_level} risk for {item.product_name}."))
        db.flush()
        responses.append(
            WastePredictionRead(
                id=prediction.id,
                inventory_item_id=item.id,
                created_at=prediction.created_at,
                **risk.__dict__,
            )
        )
    db.commit()
    return responses

