from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import AuditLog, InventoryItem, NGO, RedistributionRequest
from backend.schemas import NGORead, RedistributionRequestCreate, RedistributionResponse
from backend.services.ngo_matcher import find_best_ngo

router = APIRouter(tags=["ngos"])


@router.get("/ngos", response_model=list[NGORead])
def list_ngos(db: Session = Depends(get_db)) -> list[NGO]:
    return db.query(NGO).order_by(NGO.name.asc()).all()


@router.post("/redistribute", response_model=RedistributionResponse)
def redistribute(payload: RedistributionRequestCreate, db: Session = Depends(get_db)) -> RedistributionResponse:
    item = db.get(InventoryItem, payload.inventory_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    ngo = find_best_ngo(db, item, payload.quantity)
    if not ngo:
        return RedistributionResponse(
            inventory_item_id=item.id,
            product_name=item.product_name,
            quantity=payload.quantity,
            status="not_matched",
            message="No safe NGO match found. Expired food and non-food inventory cannot be donated.",
        )

    request = RedistributionRequest(
        inventory_item_id=item.id,
        ngo_id=ngo.id,
        quantity=payload.quantity,
        status="pending_human_approval",
    )
    db.add(request)
    db.add(AuditLog(event_type="redistribution_matched", message=f"Matched {item.product_name} to {ngo.name}."))
    db.commit()
    db.refresh(request)

    return RedistributionResponse(
        request_id=request.id,
        inventory_item_id=item.id,
        product_name=item.product_name,
        ngo_id=ngo.id,
        ngo_name=ngo.name,
        quantity=payload.quantity,
        status=request.status,
        message="Safe surplus match found. Human approval is required before pickup.",
    )

