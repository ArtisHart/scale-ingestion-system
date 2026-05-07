from app.workers.celery_app import celery
from app.db.database import SessionLocal
from app.services.ingestion_service import update_job_status
from app.models.item import Item
import requests
import logging
import csv
import os


logger = logging.getLogger(__name__)


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def process_csv_job(self, job_id: int, file_path: str):
    db = SessionLocal()

    try:
        logger.info("Starting CSV ingestion")
        update_job_status(db, job_id, "processing")

        existing_names = {i.name for i in db.query(Item.name).all()}

        count = 0

        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                name = row.get("name")
                value_raw = row.get("value")

                if not name:
                    continue

                try:
                    value = int(value_raw)
                except:
                    continue

                if name in existing_names:
                    continue

                item = Item(name=name, value=value)
                db.add(item)

                existing_names.add(name)
                count += 1

        db.commit()
        logger.info(f"Inserted {count} records")
        update_job_status(db, job_id, "completed")

    except Exception as e:
        db.rollback()
        logger.error(f"CSV job failed: {e}")
        update_job_status(db, job_id, "failed")
        raise

    finally:
        db.close()

        if os.path.exists(file_path):
            os.remove(file_path)

@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def process_api_job(self, job_id: int):
    db = SessionLocal()
    try:
        update_job_status(db, job_id, "processing")

        logger.info("Fetching API data...")

        response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=5)
        if response.status_code != 200:
            raise Exception("API failed")
        
        data = response.json()
        logger.info(f"Fetched {len(data)} records")

        existing_names = {i.name for i in db.query(Item.name).all()}

        count = 0
        for post in data[:10]:
            name = post.get("title")
            body = post.get("body")

            if not name or not body:
                continue

            if name in existing_names:
                continue

            value = len(body)

            item = Item(name=name, value=value)
            db.add(item)

            existing_names.add(name)
            count += 1
        db.commit()

        logger.info(f"Inserted {count} records")
        
        update_job_status(db, job_id, "completed")
    except Exception as e:
        update_job_status(db, job_id, "failed")
        logger.error(f"Job failed: {e}")

    finally:
        db.close()