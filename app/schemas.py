from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MetricCreate(BaseModel):
    event_name: str
    session_id: Optional[str] = None
    timestamp: Optional[datetime] = None  # si no viene, usamos utcnow del modelo

class MetricOut(BaseModel):
    id: int
    event_name: str
    user_id: int
    timestamp: datetime
    session_id: Optional[str]

    class Config:
        orm_mode = True
