from datetime import date, timedelta

from backend.database import Base, SessionLocal, engine
from backend.models import AuditLog, InventoryItem, NGO, User


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(AuditLog).delete()
        db.query(InventoryItem).delete()
        db.query(NGO).delete()
        db.query(User).delete()

        today = date.today()
        db.add(
            User(
                name="Demo Operator",
                organization_type="grocery_store",
                location="Central City",
                email="demo@wasteagent.local",
            )
        )

        items = [
            InventoryItem(product_name="Yogurt Cups", category="Dairy", quantity=120, unit="cups", expiry_date=today + timedelta(days=2), purchase_date=today - timedelta(days=5), avg_daily_sales=18, cost_per_unit=0.8, storage_condition="cold", demand_level="low", weather_factor="hot", event_factor="none"),
            InventoryItem(product_name="Fruit Juice Bottles", category="Beverage", quantity=300, unit="bottles", expiry_date=today + timedelta(days=10), purchase_date=today - timedelta(days=12), avg_daily_sales=22, cost_per_unit=1.2, storage_condition="ambient", demand_level="medium", weather_factor="normal", event_factor="negative"),
            InventoryItem(product_name="Banana Packs", category="Fruit", quantity=90, unit="packs", expiry_date=today + timedelta(days=1), purchase_date=today - timedelta(days=2), avg_daily_sales=30, cost_per_unit=0.5, storage_condition="ambient", demand_level="medium", weather_factor="hot", event_factor="none"),
            InventoryItem(product_name="Sandwich Packets", category="Prepared Food", quantity=75, unit="packets", expiry_date=today + timedelta(days=1), purchase_date=today, avg_daily_sales=12, cost_per_unit=1.5, storage_condition="cold", demand_level="low", weather_factor="rain", event_factor="low_footfall"),
            InventoryItem(product_name="Cooked Restaurant Meals", category="Restaurant Meals", quantity=65, unit="meals", expiry_date=today + timedelta(days=1), purchase_date=today, avg_daily_sales=20, cost_per_unit=2.4, storage_condition="cold", demand_level="low", weather_factor="storm", event_factor="cancellation"),
            InventoryItem(product_name="Packaged Snacks", category="Packaged Snacks", quantity=500, unit="packs", expiry_date=today + timedelta(days=90), purchase_date=today - timedelta(days=20), avg_daily_sales=35, cost_per_unit=0.6, storage_condition="ambient", demand_level="medium", weather_factor="normal", event_factor="none"),
            InventoryItem(product_name="Plastic Water Bottles", category="Plastic Beverage", quantity=900, unit="bottles", expiry_date=today + timedelta(days=180), purchase_date=today - timedelta(days=30), avg_daily_sales=25, cost_per_unit=0.35, storage_condition="ambient", demand_level="low", weather_factor="rain", event_factor="none"),
            InventoryItem(product_name="Raw Vegetables", category="Vegetables", quantity=150, unit="kg", expiry_date=today + timedelta(days=4), purchase_date=today - timedelta(days=2), avg_daily_sales=40, cost_per_unit=0.9, storage_condition="cold", demand_level="high", weather_factor="normal", event_factor="market_day"),
            InventoryItem(product_name="Milk Packets", category="Dairy", quantity=200, unit="packets", expiry_date=today + timedelta(days=3), purchase_date=today - timedelta(days=1), avg_daily_sales=70, cost_per_unit=0.7, storage_condition="cold", demand_level="high", weather_factor="hot", event_factor="none"),
            InventoryItem(product_name="Bakery Bread", category="Bakery", quantity=160, unit="loaves", expiry_date=today + timedelta(days=2), purchase_date=today - timedelta(days=1), avg_daily_sales=45, cost_per_unit=1.1, storage_condition="ambient", demand_level="medium", weather_factor="humid", event_factor="none"),
        ]
        db.add_all(items)

        ngos = [
            NGO(name="Central City Food Bank", location="Central City", accepted_categories="all_food,dairy,bakery,fruit,vegetables,prepared_food,restaurant_meals", capacity=400, contact="foodbank@example.org"),
            NGO(name="Hope Orphanage Kitchen", location="North Zone", accepted_categories="bakery,fruit,vegetables,dairy", capacity=120, contact="hope@example.org"),
            NGO(name="Night Shelter Meals Program", location="Central City", accepted_categories="prepared_food,restaurant_meals,bakery", capacity=180, contact="shelter@example.org"),
            NGO(name="Community Kitchen Network", location="East Zone", accepted_categories="all_food,vegetables,fruit,prepared_food", capacity=250, contact="kitchen@example.org"),
            NGO(name="Safe Animal Shelter Feed Program", location="South Zone", accepted_categories="fruit,vegetables,bakery", capacity=80, contact="animalsafe@example.org"),
        ]
        db.add_all(ngos)
        db.add(AuditLog(event_type="seed_completed", message="Seeded sample inventory and NGO partners."))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seed data created.")

