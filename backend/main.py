from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Job
from schemas import JobCreate, JobUpdate, JobResponse

app = FastAPI(
    title="Job Tracker API",
    description="A REST API to manage and track job applications.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Job.metadata.create_all(bind=engine)

# Home endpoint
@app.get("/", tags=["General"])
def home():
    return {"message": "Job Tracker API is running!"}

# Create Job
@app.post(
    "/jobs",
    tags=["Jobs"],
    summary="Create a new job",
    description="Create and save a new job application in the database."
)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        print("Received applied_date:", job.applied_date)

        new_job = Job(
            company=job.company,
            role=job.role,
            location=job.location,
            status=job.status,
            applied_date=job.applied_date
        )

        db.add(new_job)
        db.commit()
        db.refresh(new_job)

        return new_job

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create job"
        )

# Get All Jobs
@app.get(
    "/jobs",
    response_model=list[JobResponse],
    tags=["Jobs"],
    summary="Get all jobs",
    description="Get a list of job applications with optional filtering, searching, pagination, and sorting."
)
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

# Statistics
@app.get("/jobs/stats", tags=["Statistics"])
def get_job_stats(db: Session = Depends(get_db)):
    total = db.query(Job).count()

    applied = db.query(Job).filter(Job.status == "Applied").count()
    interview = db.query(Job).filter(Job.status == "Interview").count()
    rejected = db.query(Job).filter(Job.status == "Rejected").count()
    selected = db.query(Job).filter(Job.status == "Selected").count()

    return {
        "total": total,
        "applied": applied,
        "interview": interview,
        "rejected": rejected,
        "selected": selected
}

# Get Single Job
@app.get(
    "/jobs/{job_id}",
    response_model=JobResponse,
    tags=["Jobs"],
    summary="Get a job by ID",
    description="Get the details of a specific job application using its ID."
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

# Update Job
@app.put(
    "/jobs/{job_id}",
    response_model=JobResponse,
    tags=["Jobs"],
    summary="Update a job",
    description="Update all details of an existing job application using its ID."
)
def update_job(
    job_id: int,
    job: JobCreate,
    db: Session = Depends(get_db)
):
    existing_job = db.query(Job).filter(Job.id == job_id).first()

    if existing_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    existing_job.company = job.company
    existing_job.role = job.role
    existing_job.location = job.location
    existing_job.status = job.status
    existing_job.applied_date = job.applied_date

    try:
        db.commit()
        db.refresh(existing_job)

        return existing_job

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update job"
        )


# Delete Job
@app.delete(
    "/jobs/{job_id}",
    tags=["Jobs"],
    summary="Delete a job",
    description="Delete an existing job application using its ID."
)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    existing_job = db.query(Job).filter(Job.id == job_id).first()

    if existing_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    try:
        db.delete(existing_job)
        db.commit()

        return {
            "message": "Job deleted successfully"
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete job"
        )

# PATCH Job (update only the field(s) you want to change)
@app.patch(
    "/jobs/{job_id}",
    response_model=JobResponse,
    tags=["Jobs"],
    summary="Partially update a job",
    description="Update only the fields provided for an existing job application."
)
def patch_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db)
):
    existing_job = db.query(Job).filter(Job.id == job_id).first()

    if existing_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job.company is not None:
        existing_job.company = job.company

    if job.role is not None:
        existing_job.role = job.role

    if job.location is not None:
        existing_job.location = job.location

    if job.status is not None:
        existing_job.status = job.status

    try:
        db.commit()
        db.refresh(existing_job)

        return existing_job

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update job"
        )