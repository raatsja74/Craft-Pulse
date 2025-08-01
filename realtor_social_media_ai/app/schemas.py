from pydantic import BaseModel
from datetime import datetime

class ProfileSetup(BaseModel):
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str

class ContentRequest(BaseModel):
    content_type: str
    details: str | None = None

class GeneratedContentOut(BaseModel):
    id: int
    content_type: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class ScheduleRequest(BaseModel):
    platform: str
    content: str
    scheduled_time: datetime
