from fastapi import FastAPI
from pydantic import BaseModel

from database import engine, SessionLocal
from models import Job

app = FastAPI()

Job.metadata.create_all(bind=engine)

class JobCreate(BaseModel):
    company: str
    role: str
    location: str


@app.get("/")
def home():
    return {"message": "Job Tracker API is running!"}

#------------ CRUD OPERATIONS --------------------------

#------------C = Create--------------------------
@app.post("/jobs")
def create_job(job: JobCreate):
    db = SessionLocal()

    new_job = Job(
        company=job.company,
        role=job.role,
        location=job.location
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    db.close()

    return new_job

#------------R = Read--------------------------
@app.get("/jobs")
def get_jobs():
    db = SessionLocal()

    jobs = db.query(Job).all()

    db.close()

    return jobs

#------------U = Update--------------------------
@app.put("/jobs/{job_id}")
def update_job(job_id: int, job: JobCreate):
    db = SessionLocal()

    existing_job = db.query(Job).filter(Job.id == job_id).first()

    if existing_job is None:
        db.close()
        return {"message": "Job not found"}

    existing_job.company = job.company
    existing_job.role = job.role
    existing_job.location = job.location

    db.commit()
    db.refresh(existing_job)

    db.close()

    return existing_job


#------------D = Delete--------------------------
@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    db = SessionLocal()

    existing_job = db.query(Job).filter(Job.id == job_id).first()

    if existing_job is None:
        db.close()
        return {"message": "Job not found"}

    db.delete(existing_job)
    db.commit()

    db.close()

    return {"message": "Job deleted successfully"}