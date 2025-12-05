from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime
from .database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(Text, nullable=True)
