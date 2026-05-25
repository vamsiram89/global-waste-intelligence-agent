from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routers import actions, analytics, inventory, ngos, prediction

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Global Waste Intelligence Agent",
    description="AI that predicts and prevents waste before it is produced.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory.router)
app.include_router(prediction.router)
app.include_router(actions.router)
app.include_router(ngos.router)
app.include_router(analytics.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "global-waste-intelligence-agent"}

