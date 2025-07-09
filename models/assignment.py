from pydantic import BaseModel

class Assignment(BaseModel):
    shift_id: str
    employee_id: str
