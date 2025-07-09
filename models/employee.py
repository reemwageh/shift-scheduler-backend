from pydantic import BaseModel
from typing import List

class Availability(BaseModel):
    start: str
    end: str

class Employee(BaseModel):
    id: str
    name: str
    skills: List[str]
    max_hours: int
    availability: Availability
