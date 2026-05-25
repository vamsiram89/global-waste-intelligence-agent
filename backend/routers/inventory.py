from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import AuditLog, InventoryItem
from backend.schemas import InventoryItemCreate, InventoryItemRead

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("/add", response_model=InventoryItemRead)
def add_inventory_item(payload: InventoryItemCreate, db: Session = Depends(get_db)) -> InventoryItem:
    item = InventoryItem(**payload.model_dump())
    db.add(item)
    db.add(AuditLog(event_type="inventory_added", message=f"Added inventory item {payload.product_name}."))
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[InventoryItemRead])
def list_inventory(db: Session = Depends(get_db)) -> list[InventoryItem]:
    return db.query(InventoryItem).order_by(InventoryItem.expiry_date.asc()).all()

