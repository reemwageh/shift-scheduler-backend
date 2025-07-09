from pydantic import BaseModel
from typing import List

from models.assignment import Assignment

class Metrics(BaseModel):
    total_overtime_minutes: int
    constraint_violations: int
    optimization_time_ms: int
    objective_value: float

class ScheduleResponse(BaseModel):
    success: bool
    assignments: List[Assignment]
    unassigned_shifts: List[str]
    metrics: Metrics
    constraints_applied: List[str]