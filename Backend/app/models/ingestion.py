from sqlalchemy import Column, Integer, String
from app.db.database import Base

class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")
    source = Column(String)   # csv / api