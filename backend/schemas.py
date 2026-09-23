from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import date


class Status(str, Enum):
    Applied = "Applied"
    Interview = "Interview"
    Rejected = "Rejected"
    Selected = "Selected"


class JobCreate(BaseModel):
    company: str
    role: str
    location: str
    status: Status
    applied_date: date | None = None

class JobUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    location: str | None = None
    status: Status | None = None
    applied_date: date | None = None

class JobResponse(BaseModel):
    id: int
    company: str
    role: str
    location: str
    status: Status
    applied_date: date | None

    model_config = ConfigDict(from_attributes=True)