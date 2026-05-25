from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str
    organization_type: str
    location: str
    email: str


class InventoryItemBase(BaseModel):
    product_name: str = Field(..., examples=["Yogurt Cups"])
    category: str = Field(..., examples=["Dairy"])
    quantity: float = Field(..., ge=0)
    unit: str = Field(..., examples=["cups"])
    expiry_date: date
    purchase_date: date
    avg_daily_sales: float = Field(..., ge=0)
    cost_per_unit: float = Field(..., ge=0)
    storage_condition: str = "ambient"
    demand_level: str = "medium"
    weather_factor: str = "normal"
    event_factor: str = "none"


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemRead(InventoryItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class WastePredictionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    inventory_item_id: int | None = None
    product_name: str
    category: str
    risk_score: float
    risk_level: str
    predicted_waste_quantity: float
    estimated_loss: float
    reason: str
    days_until_expiry: int
    created_at: datetime | None = None


class ActionRequest(BaseModel):
    inventory_item_id: int


class RecommendedActionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    inventory_item_id: int
    product_name: str | None = None
    action_type: str
    action_message: str
    urgency: str
    created_at: datetime | None = None


class NGORead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    accepted_categories: str
    capacity: float
    contact: str


class RedistributionRequestCreate(BaseModel):
    inventory_item_id: int
    quantity: float = Field(..., gt=0)


class RedistributionResponse(BaseModel):
    request_id: int | None = None
    inventory_item_id: int
    product_name: str
    ngo_id: int | None = None
    ngo_name: str | None = None
    quantity: float
    status: str
    message: str


class AnalyticsSummary(BaseModel):
    total_products_monitored: int
    high_risk_products: int
    estimated_waste_value: float
    estimated_food_saved: float
    suggested_donation_quantity: float
    plastic_waste_avoided: float
    critical_alerts: list[str]
