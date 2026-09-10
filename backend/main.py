from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, SessionLocal, get_db
from models import Job

app = FastAPI()

Job.metadata.create_all(bind=engine)

class JobCreate(BaseModel):
    company: str
    role: str
    location: str
    status: str


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
        location=job.location,
        status=job.status
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    db.close()

    return new_job

#------------R = Read--------------------------
@app.get("/jobs")
def get_jobs(
    status: str = None,
    company: str = None,
    role: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Job)

    if status:
        query = query.filter(Job.status == status)

    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))

    if role:
        query = query.filter(Job.role.ilike(f"%{role}%"))

    return query.all()

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
    existing_job.status = job.status

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