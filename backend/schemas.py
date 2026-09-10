from pydantic import BaseModel


class JobCreate(BaseModel):
    company: str
    role: str
    location: str
    status: str