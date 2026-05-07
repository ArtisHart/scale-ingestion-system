from sqlalchemy.orm import Session
from app.models.ingestion import IngestionJob

def create_job(db: Session, source: str):
    job = IngestionJob(source=source, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def update_job_status(db: Session, job_id: int, status: str):
    job = db.query(IngestionJob).get(job_id)
    job.status = status
    db.commit()
    return job