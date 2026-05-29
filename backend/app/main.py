from fastapi import FastAPI
from app.api import webhook, callbacks, internal
from app.models.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lead Intelligence API")

app.include_router(webhook.router, prefix="/api/v1")
app.include_router(callbacks.router, prefix="/api/v1")
app.include_router(internal.router, prefix="/internal")

@app.get("/health")
def health():
    return {"status": "ok"}