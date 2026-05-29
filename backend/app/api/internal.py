from fastapi import APIRouter

router = APIRouter()

@router.get("/metrics")
def metrics():
    # Placeholder for Prometheus metrics
    return {"pending_review": 0, "total_conversations": 0}