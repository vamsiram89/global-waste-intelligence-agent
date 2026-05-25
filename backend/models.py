from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    organization_type: Mapped[str] = mapped_column(String(80), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_name: Mapped[str] = mapped_column(String(160), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(40), nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    purchase_date: Mapped[date] = mapped_column(Date, nullable=False)
    avg_daily_sales: Mapped[float] = mapped_column(Float, nullable=False)
    cost_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    storage_condition: Mapped[str] = mapped_column(String(80), default="ambient")
    demand_level: Mapped[str] = mapped_column(String(40), default="medium")
    weather_factor: Mapped[str] = mapped_column(String(40), default="normal")
    event_factor: Mapped[str] = mapped_column(String(40), default="none")

    predictions: Mapped[list["WastePrediction"]] = relationship(back_populates="inventory_item")
    actions: Mapped[list["RecommendedAction"]] = relationship(back_populates="inventory_item")


class WastePrediction(Base):
    __tablename__ = "waste_predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    inventory_item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(40), nullable=False)
    predicted_waste_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_loss: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    inventory_item: Mapped[InventoryItem] = relationship(back_populates="predictions")


class RecommendedAction(Base):
    __tablename__ = "recommended_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    inventory_item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"), nullable=False)
    action_type: Mapped[str] = mapped_column(String(80), nullable=False)
    action_message: Mapped[str] = mapped_column(Text, nullable=False)
    urgency: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    inventory_item: Mapped[InventoryItem] = relationship(back_populates="actions")


class NGO(Base):
    __tablename__ = "ngos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    accepted_categories: Mapped[str] = mapped_column(Text, nullable=False)
    capacity: Mapped[float] = mapped_column(Float, nullable=False)
    contact: Mapped[str] = mapped_column(String(160), nullable=False)


class RedistributionRequest(Base):
    __tablename__ = "redistribution_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    inventory_item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"), nullable=False)
    ngo_id: Mapped[int] = mapped_column(ForeignKey("ngos.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(60), default="pending_human_approval")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

