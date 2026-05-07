from fastapi import FastAPI, Depends, UploadFile, File
from app.db.database import Base, engine, get_db
from sqlalchemy.orm import Session
from app.schemas.item import ItemCreate, ItemResponse
from app.services.item_service import create_item, get_items
from app.schemas.ingestion import IngestionResponse, IngestionCreate
from app.services.ingestion_service import create_job, update_job_status
from app.models.ingestion import IngestionJob
from app.workers.tasks import process_api_job, process_csv_job
import shutil
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/items", response_model=ItemResponse)
def create_item_route(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@app.get("/items", response_model=list[ItemResponse])
def get_items_route(db: Session = Depends(get_db)):
    return get_items(db)

@app.post("/ingest-csv")
def ingest_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    job = create_job(db, source="csv")

    # save file locally (temp)
    file_location = f"/shared/temp_{job.id}.csv"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    process_csv_job.delay(job.id, file_location)

    return {"job_id": job.id, "status": "pending"}

@app.post("/ingest-api", response_model=IngestionResponse)
def ingest_api(db: Session = Depends(get_db)):
    job = create_job(db, source = "api")

    process_api_job.delay(job.id)

    return {"id": job.id, "source": job.source, "status": "pending"}

@app.get("/ingest", response_model=IngestionResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return db.query(IngestionJob).get(job_id)