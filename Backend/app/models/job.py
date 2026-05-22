from app.db.database import Base
from sqlalchemy import Column, Integer, String

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    status = Column(String)