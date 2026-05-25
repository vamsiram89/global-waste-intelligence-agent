import html
import os
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Global Waste Intelligence Agent",
    page_icon="GW",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_theme():
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

          :root {
            --ink: #07111f;
            --panel: rgba(255, 255, 255, 0.90);
            --panel-strong: #ffffff;
            --muted: #637083;
            --line: rgba(15, 23, 42, 0.10);
            --blue: #2563eb;
            --leaf: #16a34a;
            --amber: #d97706;
            --red: #dc2626;
            --cyan: #0891b2;
          }

          html, body, [class*="css"] {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          }

          .stApp {
            color: var(--ink);
            background:
              linear-gradient(135deg, rgba(37, 99, 235, 0.08), transparent 32%),
              linear-gradient(315deg, rgba(22, 163, 74, 0.10), transparent 26%),
              #eef4f8;
          }

          .block-container {
            max-width: 1500px;
            padding-top: 1.6rem;
            padding-bottom: 3rem;
          }

          [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #07111f 0%, #10243b 58%, #0f2f27 100%);
            border-right: 1px solid rgba(255,255,255,0.10);
          }

          [data-testid="stSidebar"] * {
            color: #f8fafc;
          }

          [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: rgba(248, 250, 252, 0.78);
          }

          [data-testid="stSidebar"] label {
            color: rgba(248, 250, 252, 0.62) !important;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.74rem;
          }

          [data-testid="stSidebar"] [role="radiogroup"] {
            display: grid;
            gap: 0.35rem;
          }

          [data-testid="stSidebar"] [role="radiogroup"] label {
            min-height: 2.75rem;
            border-radius: 0.9rem;
            padding: 0.45rem 0.65rem;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            text-transform: none;
            letter-spacing: 0;
          }

          [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255,255,255,0.12);
          }

          [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(135deg, #2563eb, #0891b2);
            border-color: rgba(255,255,255,0.22);
            box-shadow: 0 12px 32px rgba(37, 99, 235, 0.30);
          }

          h1, h2, h3 {
            color: var(--ink);
            letter-spacing: 0;
          }

          .premium-shell {
            display: grid;
            grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr);
            gap: 1rem;
            align-items: stretch;
            margin-bottom: 1.1rem;
          }

          .hero-panel, .premium-card {
            border: 1px solid rgba(255,255,255,0.84);
            background: var(--panel);
            box-shadow: 0 24px 70px rgba(15, 23, 42, 0.10);
            backdrop-filter: blur(18px);
          }

          .hero-panel {
            min-height: 250px;
            border-radius: 1.5rem;
            padding: 1.4rem;
            position: relative;
            overflow: hidden;
            background:
              linear-gradient(135deg, rgba(7, 17, 31, 0.94), rgba(14, 54, 67, 0.86)),
              radial-gradient(circle at 88% 20%, rgba(34, 197, 94, 0.28), transparent 16rem);
          }

          .hero-panel * {
            color: white;
            position: relative;
            z-index: 1;
          }

          .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            border-radius: 999px;
            padding: 0.45rem 0.75rem;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.16);
            font-size: 0.78rem;
            font-weight: 800;
          }

          .hero-title {
            margin: 1.2rem 0 0.65rem;
            max-width: 760px;
            font-size: clamp(2.1rem, 4.4vw, 4.7rem);
            line-height: 0.98;
            font-weight: 900;
          }

          .hero-copy {
            max-width: 760px;
            color: rgba(255,255,255,0.78);
            font-size: 1.02rem;
            line-height: 1.7;
          }

          .hero-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            margin-top: 1.15rem;
          }

          .hero-pill {
            border-radius: 999px;
            padding: 0.58rem 0.78rem;
            background: rgba(255,255,255,0.11);
            border: 1px solid rgba(255,255,255,0.12);
            font-size: 0.82rem;
            font-weight: 800;
          }

          .side-status {
            border-radius: 1.5rem;
            padding: 1.2rem;
          }

          .status-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.9rem 0;
            border-bottom: 1px solid var(--line);
          }

          .status-row:last-child {
            border-bottom: 0;
          }

          .status-label {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 700;
          }

          .status-value {
            color: var(--ink);
            font-weight: 900;
            text-align: right;
          }

          .metric-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
          }

          .metric-value {
            margin-top: 0.55rem;
            color: var(--ink);
            font-size: 1.8rem;
            font-weight: 900;
          }

          .metric-help {
            margin-top: 0.35rem;
            color: var(--muted);
            font-size: 0.8rem;
          }

          .section-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin: 1.5rem 0 0.8rem;
          }

          .section-title h2 {
            margin: 0;
            font-size: 1.35rem;
            font-weight: 900;
          }

          .section-title p {
            margin: 0.25rem 0 0;
            color: var(--muted);
          }

          .premium-card {
            border-radius: 1.2rem;
            padding: 1rem;
            margin-bottom: 1rem;
          }

          .risk-badge {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.32rem 0.62rem;
            font-size: 0.72rem;
            font-weight: 900;
            text-transform: uppercase;
            border: 1px solid transparent;
          }

          .risk-low { color: #047857; background: #dcfce7; border-color: #86efac; }
          .risk-medium { color: #92400e; background: #fef3c7; border-color: #fcd34d; }
          .risk-high { color: #9a3412; background: #ffedd5; border-color: #fdba74; }
          .risk-critical { color: #991b1b; background: #fee2e2; border-color: #fca5a5; }

          .alert-card {
            border-radius: 1rem;
            padding: 0.95rem;
            background: white;
            border: 1px solid var(--line);
            box-shadow: 0 12px 32px rgba(15, 23, 42, 0.06);
          }

          .alert-title {
            display: flex;
            justify-content: space-between;
            gap: 0.7rem;
            align-items: center;
            font-weight: 900;
          }

          .alert-meta {
            margin-top: 0.45rem;
            color: var(--muted);
            line-height: 1.45;
            font-size: 0.88rem;
          }

          .stButton > button, .stFormSubmitButton > button {
            border: 0;
            border-radius: 0.9rem;
            background: linear-gradient(135deg, #2563eb, #0891b2);
            color: #ffffff;
            font-weight: 900;
            min-height: 2.75rem;
            box-shadow: 0 15px 38px rgba(37, 99, 235, 0.22);
          }

          .stButton > button *, .stFormSubmitButton > button * {
            color: #ffffff !important;
          }

          .stButton > button:hover, .stFormSubmitButton > button:hover {
            color: white;
            border: 0;
            transform: translateY(-1px);
          }

          [data-testid="stDataFrame"], [data-testid="stTable"] {
            border-radius: 1rem;
            overflow: hidden;
            border: 1px solid var(--line);
            box-shadow: 0 16px 44px rgba(15, 23, 42, 0.07);
          }

          div[data-testid="stMetric"] {
            border-radius: 1rem;
            padding: 1rem;
            background: white;
            border: 1px solid var(--line);
          }

          div[data-testid="stMetric"] label,
          div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            color: #475569 !important;
            font-weight: 800;
          }

          div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #07111f !important;
            font-weight: 900;
          }

          .stAlert {
            border-radius: 0.9rem;
          }

          .stAlert, .stAlert * {
            color: #07111f !important;
            font-weight: 650;
          }

          [data-testid="stDataFrame"], [data-testid="stDataFrame"] * {
            color: #07111f;
          }

          [data-testid="stSelectbox"] label,
          [data-testid="stNumberInput"] label,
          [data-testid="stTextInput"] label,
          [data-testid="stDateInput"] label {
            color: #334155 !important;
            font-weight: 800;
          }

          @media (max-width: 1100px) {
            .premium-shell {
              grid-template-columns: 1fr;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


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


def money(value: float | int) -> str:
    return f"${float(value):,.0f}"


def clean_label(value: str) -> str:
    return str(value).replace("_", " ").strip().title()


def clean_category_list(value: str) -> str:
    categories = [clean_label(part) for part in str(value).split(",") if part.strip()]
    return ", ".join(categories)


def risk_badge(level: str) -> str:
    key = str(level).lower().replace(" ", "_")
    css_key = key if key in {"low", "medium", "high", "critical"} else "medium"
    return f"<span class='risk-badge risk-{css_key}'>{html.escape(clean_label(str(level)))}</span>"


def render_sidebar():
    st.sidebar.markdown(
        """
        <div style="padding: 0.75rem 0 1.2rem;">
          <div style="display:flex;align-items:center;gap:0.75rem;">
            <div style="width:2.75rem;height:2.75rem;border-radius:0.9rem;background:linear-gradient(135deg,#22c55e,#38bdf8);display:grid;place-items:center;font-weight:900;">GW</div>
            <div>
              <div style="font-size:1rem;font-weight:900;color:#fff;">Waste Intelligence</div>
              <div style="font-size:0.78rem;color:rgba(255,255,255,0.62);">MVP command center</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(page: str, summary: dict | None = None):
    high_risk = (summary or {}).get("high_risk_products", "Ready")
    monitored = (summary or {}).get("total_products_monitored", "Live")
    loss = money((summary or {}).get("estimated_waste_value", 0))
    st.markdown(
        f"""
        <div class="premium-shell">
          <section class="hero-panel">
            <div class="eyebrow">Explainable prevention engine - {html.escape(page)}</div>
            <h1 class="hero-title">Global Waste Intelligence Agent</h1>
            <p class="hero-copy">
              Predict inventory, food, plastic, and production waste before it happens.
              Every recommendation stays explainable, safety-aware, and ready for human approval.
            </p>
            <div class="hero-strip">
              <span class="hero-pill">No expired-food donations</span>
              <span class="hero-pill">Human approval required</span>
              <span class="hero-pill">Rule-based MVP logic</span>
            </div>
          </section>
          <aside class="premium-card side-status">
            <div class="status-row">
              <div class="status-label">Backend</div>
              <div class="status-value">{html.escape(API_BASE_URL)}</div>
            </div>
            <div class="status-row">
              <div class="status-label">Products monitored</div>
              <div class="status-value">{monitored}</div>
            </div>
            <div class="status-row">
              <div class="status-label">High-risk products</div>
              <div class="status-value">{high_risk}</div>
            </div>
            <div class="status-row">
              <div class="status-label">Estimated loss</div>
              <div class="status-value">{loss}</div>
            </div>
          </aside>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_grid(summary: dict):
    cards = [
        ("Products monitored", summary.get("total_products_monitored", 0), "Inventory items under risk scoring"),
        ("High-risk products", summary.get("high_risk_products", 0), "Needs action before expiry or overstock"),
        ("Estimated loss", money(summary.get("estimated_waste_value", 0)), "Predicted value at risk"),
        ("Food saved", f"{summary.get('estimated_food_saved', 0):,.1f}", "Units protected by prevention"),
        ("Plastic avoided", f"{summary.get('plastic_waste_avoided', 0):,.1f} kg", "Estimated packaging avoided"),
    ]
    columns = st.columns(len(cards))
    for column, (label, value, help_text) in zip(columns, cards):
        column.metric(label, value, help=help_text)


def section(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="section-title">
          <div>
            <h2>{html.escape(title)}</h2>
            <p>{html.escape(subtitle)}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_alert_cards(predictions: list[dict], limit: int = 4):
    if not predictions:
        st.info("No live alerts yet. Add inventory and run predictions to populate this feed.")
        return

    ordered = sorted(predictions, key=lambda item: item.get("risk_score", 0), reverse=True)[:limit]
    columns = st.columns(min(limit, len(ordered)))
    for column, item in zip(columns, ordered):
        with column:
            st.markdown(
                f"""
                <div class="alert-card">
                  <div class="alert-title">
                    <span>{html.escape(item.get("product_name", "Unknown item"))}</span>
                    {risk_badge(item.get("risk_level", "Medium"))}
                  </div>
                  <div class="metric-value" style="font-size:1.65rem;">{item.get("risk_score", 0):.0f}</div>
                  <div class="alert-meta">{html.escape(item.get("reason", "No explanation returned."))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def risk_chart(df: pd.DataFrame):
    color_map = {
        "Low": "#22c55e",
        "Medium": "#f59e0b",
        "High": "#f97316",
        "Critical": "#ef4444",
        "low": "#22c55e",
        "medium": "#f59e0b",
        "high": "#f97316",
        "critical": "#ef4444",
    }
    fig = px.bar(
        df.sort_values("risk_score", ascending=False),
        x="product_name",
        y="risk_score",
        color="risk_level",
        color_discrete_map=color_map,
        hover_data=["category", "predicted_waste_quantity", "estimated_loss", "reason"],
    )
    fig.update_layout(
        height=430,
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font={"family": "Inter", "color": "#07111f"},
        margin={"l": 12, "r": 12, "t": 12, "b": 12},
        legend_title_text="Risk level",
        xaxis_title="",
        yaxis_title="Risk score",
        bargap=0.26,
    )
    fig.update_traces(marker_line_width=0, opacity=0.94)
    fig.update_xaxes(showgrid=False, tickangle=-28, tickfont={"color": "#07111f"}, title_font={"color": "#07111f"})
    fig.update_yaxes(gridcolor="rgba(15,23,42,0.18)", zeroline=False, tickfont={"color": "#07111f"}, title_font={"color": "#07111f"})
    st.plotly_chart(fig, use_container_width=True)


inject_theme()
summary = safe_api(lambda: api_get("/analytics/summary"), {})
render_sidebar()

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

if page in {"Home / Overview", "Analytics", "Demo Scenarios"}:
    render_hero(page, summary)

if page == "Home / Overview":
    render_metric_grid(summary or {})
    predictions = load_predictions()
    section("Priority Risk Watch", "Highest risk items with clear rule-based explanations")
    render_alert_cards(predictions)
    st.info("Safety note: real deployments need food safety validation, local compliance, and human approval before donation pickup.")

elif page == "Inventory":
    section("Inventory Dashboard", "Add products and review the operational stock used by the prediction engine")
    section("Add Product", "Capture expiry, sales velocity, storage, demand, weather, and event signals")
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

    section("Current Inventory", "Operational stock view used by the prediction engine")
    items = load_inventory()
    if items:
        st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
    else:
        st.info("No inventory added yet.")

elif page == "Waste Prediction":
    predictions = load_predictions()
    section("Waste Risk Scores", "Live risk scores, predicted loss, and explainable reasons")
    if predictions:
        df = pd.DataFrame(predictions)
        render_alert_cards(predictions)
        st.dataframe(
            df[["product_name", "category", "risk_score", "risk_level", "predicted_waste_quantity", "estimated_loss", "days_until_expiry", "reason"]],
            use_container_width=True,
            hide_index=True,
        )
        section("Risk by Product", "Color-coded by risk level")
        risk_chart(df)
    else:
        st.info("No stored predictions yet. Add inventory items first.")

elif page == "Action Recommendation":
    section("Generate Prevention Action", "Discount, reduce-order, recycle, or redistribution guidance with safety checks")
    st.warning("Redistribution actions require human approval in this MVP. Never donate expired food.")
    items = load_inventory()
    options = inventory_options(items)
    if options:
        selected = st.selectbox("Select product", list(options))
        if st.button("Recommend action"):
            action = safe_api(lambda: api_post("/actions/recommend", {"inventory_item_id": options[selected]}))
            if action:
                action_name = clean_label(action["action_type"])
                st.success(action_name)
                st.markdown(
                    f"""
                    <div class="premium-card">
                      <div class="alert-title">
                        <span>{html.escape(action_name)}</span>
                        {risk_badge(action.get("urgency", "recommended"))}
                      </div>
                      <div class="alert-meta">{html.escape(action["action_message"])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("Add inventory first to generate recommendations.")

elif page == "NGO Matching":
    section("Redistribution Partner Matching", "Find safe partner candidates while keeping approval in human hands")
    st.warning("The MVP blocks expired-food donation recommendations and keeps redistribution pending for human approval.")
    ngos = safe_api(lambda: api_get("/ngos"), [])
    if ngos:
        ngo_df = pd.DataFrame(ngos)
        if "accepted_categories" in ngo_df:
            ngo_df["accepted_categories"] = ngo_df["accepted_categories"].map(clean_category_list)
        ngo_df = ngo_df.rename(
            columns={
                "id": "ID",
                "name": "Partner",
                "location": "Location",
                "accepted_categories": "Accepted categories",
            }
        )
        st.dataframe(ngo_df, use_container_width=True, hide_index=True)

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
                    st.markdown(f"**Matched NGO:** {html.escape(result['ngo_name'])}")
                else:
                    st.warning(result["message"])
    else:
        st.info("Add inventory first to test redistribution matching.")

elif page == "Analytics":
    section("Waste Intelligence Analytics", "Portfolio-level loss, risk, food, and plastic prevention signals")
    if summary:
        render_metric_grid(summary)
    predictions = load_predictions()
    if predictions:
        df = pd.DataFrame(predictions)
        category_df = df.groupby("category", as_index=False)["risk_score"].mean()
        loss_df = df.groupby("category", as_index=False)["estimated_loss"].sum()
        cols = st.columns(2)
        with cols[0]:
            fig = px.bar(category_df, x="category", y="risk_score", color="risk_score", color_continuous_scale="Tealgrn")
            fig.update_layout(
                title="",
                template="plotly_white",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0)",
                font={"family": "Inter", "color": "#07111f"},
                height=380,
            )
            fig.update_xaxes(tickfont={"color": "#07111f"}, title_font={"color": "#07111f"})
            fig.update_yaxes(gridcolor="rgba(15,23,42,0.18)", tickfont={"color": "#07111f"}, title_font={"color": "#07111f"})
            st.plotly_chart(fig, use_container_width=True)
        with cols[1]:
            fig = px.pie(loss_df, names="category", values="estimated_loss", hole=0.55, color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(
                title="",
                template="plotly_white",
                paper_bgcolor="rgba(0,0,0,0)",
                font={"family": "Inter", "color": "#07111f"},
                height=380,
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No prediction analytics available yet.")

elif page == "Demo Scenarios":
    section("Portfolio Demo Scenarios", "One-click examples for supermarkets, restaurants, factories, warehouses, and homes")
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
                    cols = st.columns(3)
                    cols[0].metric("Risk score", result["risk_score"])
                    cols[1].metric("Risk level", result["risk_level"])
                    cols[2].metric("Estimated loss", money(result.get("estimated_loss", 0)))
                    st.write(result["reason"])
