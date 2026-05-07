# 🚀 Scalable Data Ingestion System

A distributed backend system that ingests data from external APIs and files, processes it asynchronously, and stores it in a relational database.

## 🧠 Overview

This project demonstrates a production-style ingestion pipeline using:

- FastAPI (API layer)
- Celery (asynchronous task processing)
- Redis (message broker)
- PostgreSQL (data storage)
- Docker Compose (container orchestration)

## ⚙️ Architecture

Client → FastAPI → Redis Queue → Celery Worker → PostgreSQL

- API handles requests and enqueues jobs
- Redis acts as a message broker
- Celery workers process jobs asynchronously
- Data is transformed and stored in PostgreSQL

## 🔥 Features

- Asynchronous job processing using Celery
- External API ingestion (JSONPlaceholder)
- CSV file ingestion support
- Idempotent data handling (duplicate prevention)
- Retry logic for fault tolerance
- Structured logging
- Dockerized multi-service architecture

## 🛠️ Tech Stack

- Python
- FastAPI
- Celery
- Redis
- PostgreSQL
- Docker / Docker Compose
- SQLAlchemy

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/scale-ingestion-system.git
cd scale-ingestion-system
```
