from enum import Enum
from pydantic import BaseModel


class JobStatus(str, Enum):
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    REJECTED = "Rejected"
    SELECTED = "Selected"


class JobCreate(BaseModel):
    company: str
    role: str
    location: str
    status: JobStatus


class JobUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    location: str | None = None
    status: JobStatus | None = None


class JobResponse(BaseModel):
    id: int
    company: str
    role: str
    location: str
    status: JobStatus

    class Config:
        from_attributes = True