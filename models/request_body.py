from pydantic import BaseModel
from typing import List, Optional

from models.employee import Employee
from models.shift import Shift

class CurrentAssignment(BaseModel):
    shift_id: str
    employee_id: str
class ScheduleRequest(BaseModel):
    period: str
    employees: List[Employee]
    shifts: List[Shift]
    current_assignments: Optional[List[CurrentAssignment]] = []
    max_shifts_per_day: Optional[int] = 2
    min_rest_between_shifts: Optional[int] = 12 