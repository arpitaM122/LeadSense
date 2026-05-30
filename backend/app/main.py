from fastapi import FastAPI
from .api import webhook, callbacks, internal
from .models.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lead Intelligence API")

#  ADD THIS LINE
@app.get("/")
def root():
    return {"message": "Lead Intelligence API is running", "status": "ok"}

app.include_router(webhook.router, prefix="/api/v1")
app.include_router(callbacks.router, prefix="/api/v1")
app.include_router(internal.router, prefix="/internal")

@app.get("/health")
def health():
    return {"status": "ok"}