from fastapi import APIRouter, HTTPException
from models.request_body import ScheduleRequest
from services.optimizer import optimize_schedule

router = APIRouter()

@router.get("/api/health")
def health_check():
    return {"status": "ok"}

@router.post("/schedule/optimize")
def run_optimization(data: ScheduleRequest):
    try:
        response = optimize_schedule(data)
        return response.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))