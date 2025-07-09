from pydantic import BaseModel

class Shift(BaseModel):
    id: str
    role: str
    start_time: str
    end_time: str
    required_skill: str
