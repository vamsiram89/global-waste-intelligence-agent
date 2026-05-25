import os
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Global Waste Intelligence Agent", layout="wide")


def api_get(path: str):
    response = requests.get(f"{API_BASE_URL}{path}", timeout=10)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload: dict):
    response = requests.post(f"{API_BASE_URL}{path}", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def safe_api(callable_fn, fallback=None):
    try:
        return callable_fn()
    except requests.RequestException as exc:
        st.error(f"Backend request failed: {exc}")
        st.info("Start the API with: uvicorn backend.main:app --reload --port 8000")
        return fallback


def load_inventory() -> list[dict]:
    return safe_api(lambda: api_get("/inventory"), [])


def load_predictions() -> list[dict]:
    return safe_api(lambda: api_get("/predict/all"), [])


def inventory_options(items: list[dict]) -> dict[str, int]:
    return {f"{item['product_name']} ({item['category']})": item["id"] for item in items}


def render_metric_grid(summary: dict):
    cols = st.columns(5)
    cols[0].metric("Products monitored", summary.get("total_products_monitored", 0))
    cols[1].metric("High-risk products", summary.get("high_risk_products", 0))
    cols[2].metric("Estimated loss", f"${summary.get('estimated_waste_value', 0):,.2f}")
    cols[3].metric("Food saved", f"{summary.get('estimated_food_saved', 0):,.1f}")
    cols[4].metric("Plastic avoided", f"{summary.get('plastic_waste_avoided', 0):,.1f}")


st.sidebar.title("Waste Intelligence")
page = st.sidebar.radio(
    "Navigate",
    [
        "Home / Overview",
        "Inventory",
        "Waste Prediction",
        "Action Recommendation",
        "NGO Matching",
        "Analytics",
        "Demo Scenarios",
    ],
)

st.title("Global Waste Intelligence Agent")
st.caption("AI that reduces waste before it is produced")

if page == "Home / Overview":
    st.subheader("Mission")
    st.write(
        "Predict waste risk early, explain why it may happen, and recommend prevention actions before food, plastic, inventory, or production becomes waste."
    )
    summary = safe_api(lambda: api_get("/analytics/summary"), {})
    if summary:
        render_metric_grid(summary)
        if summary.get("critical_alerts"):
            st.warning("Critical alerts: " + ", ".join(summary["critical_alerts"]))
    st.info("Safety note: real deployments need food safety validation, local compliance, and human approval before donation pickup.")

elif page == "Inventory":
    st.subheader("Add Product")
    with st.form("inventory_form"):
        cols = st.columns(3)
        product_name = cols[0].text_input("Product name", "Yogurt Cups")
        category = cols[1].selectbox(
            "Category",
            ["Dairy", "Fruit", "Vegetables", "Prepared Food", "Restaurant Meals", "Bakery", "Beverage", "Packaged Snacks", "Plastic Beverage"],
        )
        quantity = cols[2].number_input("Quantity", min_value=0.0, value=120.0)
        cols = st.columns(3)
        unit = cols[0].text_input("Unit", "cups")
        expiry_date = cols[1].date_input("Expiry date", date.today() + timedelta(days=2))
        purchase_date = cols[2].date_input("Purchase date", date.today())
        cols = st.columns(3)
        avg_daily_sales = cols[0].number_input("Average daily sales", min_value=0.0, value=18.0)
        cost_per_unit = cols[1].number_input("Cost per unit", min_value=0.0, value=0.8)
        storage_condition = cols[2].selectbox("Storage", ["ambient", "cold", "frozen", "controlled", "poor", "warm"])
        cols = st.columns(3)
        demand_level = cols[0].selectbox("Demand", ["low", "medium", "high"])
        weather_factor = cols[1].selectbox("Weather", ["normal", "hot", "humid", "rain", "storm", "heatwave"])
        event_factor = cols[2].selectbox("Event impact", ["none", "negative", "low_footfall", "cancellation", "festival", "market_day"])
        submitted = st.form_submit_button("Add inventory item")
        if submitted:
            payload = {
                "product_name": product_name,
                "category": category,
                "quantity": quantity,
                "unit": unit,
                "expiry_date": expiry_date.isoformat(),
                "purchase_date": purchase_date.isoformat(),
                "avg_daily_sales": avg_daily_sales,
                "cost_per_unit": cost_per_unit,
                "storage_condition": storage_condition,
                "demand_level": demand_level,
                "weather_factor": weather_factor,
                "event_factor": event_factor,
            }
            created = safe_api(lambda: api_post("/inventory/add", payload))
            if created:
                st.success(f"Added {created['product_name']}")

    st.subheader("Current Inventory")
    items = load_inventory()
    if items:
        st.dataframe(pd.DataFrame(items), use_container_width=True)

elif page == "Waste Prediction":
    st.subheader("Waste Risk Scores")
    predictions = load_predictions()
    if predictions:
        df = pd.DataFrame(predictions)
        st.dataframe(
            df[["product_name", "category", "risk_score", "risk_level", "predicted_waste_quantity", "estimated_loss", "days_until_expiry", "reason"]],
            use_container_width=True,
        )
        fig = px.bar(df, x="product_name", y="risk_score", color="risk_level", title="Waste Risk by Product")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Action Recommendation":
    st.subheader("Generate Prevention Action")
    items = load_inventory()
    options = inventory_options(items)
    if options:
        selected = st.selectbox("Select product", list(options))
        if st.button("Recommend action"):
            action = safe_api(lambda: api_post("/actions/recommend", {"inventory_item_id": options[selected]}))
            if action:
                st.success(action["action_type"])
                st.write(action["action_message"])
                st.metric("Urgency", action["urgency"].upper())

elif page == "NGO Matching":
    st.subheader("Redistribution Partner Matching")
    ngos = safe_api(lambda: api_get("/ngos"), [])
    if ngos:
        st.dataframe(pd.DataFrame(ngos), use_container_width=True)

    items = load_inventory()
    options = inventory_options(items)
    if options:
        selected = st.selectbox("Product to redistribute", list(options))
        quantity = st.number_input("Donation quantity", min_value=1.0, value=25.0)
        if st.button("Find NGO match"):
            result = safe_api(lambda: api_post("/redistribute", {"inventory_item_id": options[selected], "quantity": quantity}))
            if result:
                if result["status"] == "pending_human_approval":
                    st.success(result["message"])
                    st.write(f"Matched NGO: {result['ngo_name']}")
                else:
                    st.warning(result["message"])

elif page == "Analytics":
    st.subheader("Waste Intelligence Analytics")
    summary = safe_api(lambda: api_get("/analytics/summary"), {})
    if summary:
        render_metric_grid(summary)
    predictions = load_predictions()
    if predictions:
        df = pd.DataFrame(predictions)
        category_df = df.groupby("category", as_index=False)["risk_score"].mean()
        loss_df = df.groupby("category", as_index=False)["estimated_loss"].sum()
        st.plotly_chart(px.bar(category_df, x="category", y="risk_score", title="Average Waste Risk by Category"), use_container_width=True)
        st.plotly_chart(px.pie(loss_df, names="category", values="estimated_loss", title="Predicted Loss by Category"), use_container_width=True)

elif page == "Demo Scenarios":
    st.subheader("Portfolio Demo Scenarios")
    scenarios = [
        {
            "title": "Supermarket yogurt expiry",
            "payload": {"product_name": "Demo Yogurt Cups", "category": "Dairy", "quantity": 160, "unit": "cups", "expiry_date": (date.today() + timedelta(days=2)).isoformat(), "purchase_date": (date.today() - timedelta(days=4)).isoformat(), "avg_daily_sales": 16, "cost_per_unit": 0.8, "storage_condition": "cold", "demand_level": "low", "weather_factor": "hot", "event_factor": "none"},
        },
        {
            "title": "Restaurant unsold meals",
            "payload": {"product_name": "Demo Unsold Meals", "category": "Restaurant Meals", "quantity": 80, "unit": "meals", "expiry_date": (date.today() + timedelta(days=1)).isoformat(), "purchase_date": date.today().isoformat(), "avg_daily_sales": 15, "cost_per_unit": 2.4, "storage_condition": "cold", "demand_level": "low", "weather_factor": "storm", "event_factor": "cancellation"},
        },
        {
            "title": "Factory juice overproduction",
            "payload": {"product_name": "Demo Juice Bottles", "category": "Beverage", "quantity": 700, "unit": "bottles", "expiry_date": (date.today() + timedelta(days=20)).isoformat(), "purchase_date": (date.today() - timedelta(days=3)).isoformat(), "avg_daily_sales": 18, "cost_per_unit": 1.1, "storage_condition": "ambient", "demand_level": "low", "weather_factor": "rain", "event_factor": "negative"},
        },
        {
            "title": "Warehouse packaged snacks",
            "payload": {"product_name": "Demo Packaged Snacks", "category": "Packaged Snacks", "quantity": 950, "unit": "packs", "expiry_date": (date.today() + timedelta(days=80)).isoformat(), "purchase_date": (date.today() - timedelta(days=20)).isoformat(), "avg_daily_sales": 20, "cost_per_unit": 0.6, "storage_condition": "ambient", "demand_level": "medium", "weather_factor": "normal", "event_factor": "none"},
        },
        {
            "title": "Home grocery waste",
            "payload": {"product_name": "Demo Home Vegetables", "category": "Vegetables", "quantity": 12, "unit": "kg", "expiry_date": (date.today() + timedelta(days=3)).isoformat(), "purchase_date": (date.today() - timedelta(days=2)).isoformat(), "avg_daily_sales": 2, "cost_per_unit": 0.9, "storage_condition": "cold", "demand_level": "low", "weather_factor": "humid", "event_factor": "none"},
        },
    ]
    for scenario in scenarios:
        with st.expander(scenario["title"]):
            st.json(scenario["payload"])
            if st.button(f"Predict {scenario['title']}"):
                result = safe_api(lambda payload=scenario["payload"]: api_post("/predict/waste-risk", payload))
                if result:
                    st.metric("Risk score", result["risk_score"])
                    st.write(result["risk_level"])
                    st.write(result["reason"])
