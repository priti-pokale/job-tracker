from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, SessionLocal, get_db
from models import Job
from schemas import JobCreate, JobUpdate, JobResponse

app = FastAPI()

Job.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Job Tracker API is running!"}

#------------ CRUD OPERATIONS --------------------------

#------------C = Create--------------------------
@app.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):

    new_job = Job(
        company=job.company,
        role=job.role,
        location=job.location,
        status=job.status
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

#------------R = Read--------------------------
@app.get("/jobs", response_model=list[JobResponse])
@app.get("/jobs", response_model=list[JobResponse])
def get_jobs(
    status: str = None,
    company: str = None,
    role: str = None,
    search: str = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    query = db.query(Job)

    if status:
        query = query.filter(Job.status == status)

    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))

    if role:
        query = query.filter(Job.role.ilike(f"%{role}%"))

    if search:
        query = query.filter(
            (Job.company.ilike(f"%{search}%")) |
            (Job.role.ilike(f"%{search}%")) |
            (Job.location.ilike(f"%{search}%"))
        )

    if sort_by == "company":
        sort_column = Job.company
    elif sort_by == "role":
        sort_column = Job.role
    elif sort_by == "status":
        sort_column = Job.status
    else:
        sort_column = Job.id

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    jobs = query.offset(skip).limit(limit).all()

    return jobs

#------------U = Update--------------------------
@app.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job: JobCreate,
    db: Session = Depends(get_db)
):
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
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    existing_job = db.query(Job).filter(Job.id == job_id).first()

    if existing_job is None:
        db.close()
        return {"message": "Job not found"}

    db.delete(existing_job)
    db.commit()

    db.close()

    return {"message": "Job deleted successfully"}

#------------ PATCH (update only the field(s) you want to change) --------------------------
@app.patch("/jobs/{job_id}", response_model=JobResponse)
def patch_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db)
):
    existing_job = db.query(Job).filter(Job.id == job_id).first()

    if existing_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.company is not None:
        existing_job.company = job.company

    if job.role is not None:
        existing_job.role = job.role

    if job.location is not None:
        existing_job.location = job.location

    if job.status is not None:
        existing_job.status = job.status

    db.commit()
    db.refresh(existing_job)

    return existing_job