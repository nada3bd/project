from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PatientCreate(BaseModel):
    name: str
    room_number: str

class VisionCreate(BaseModel):
    patient_id: int
    eye_state: str
    posture: str
    people_count: int
    person_type: str

class VisionResponse(VisionCreate):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True