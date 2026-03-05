from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    question = Column(String)
    nb_sources = Column(Integer)
    duration_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())