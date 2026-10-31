
from pydantic import BaseModel, Field,ConfigDict
from datetime import date
from typing import Literal


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)
    application_date: date
    status: Literal[
        "Applied",
        "Interview",
        "Offer",
        "Rejected"
    ] = "Applied"

class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=100)
    role: str | None = Field(default=None, min_length=1, max_length=100)
    application_date: date | None = None
    status: Literal[
        "Applied",
        "Interview",
        "Offer",
        "Rejected"
    ] | None = None
class ApplicationResponse(BaseModel):
    id: str
    company: str
    role: str
    application_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)

class UserRegister(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: str
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

from datetime import datetime
from typing import Literal


class InterviewCreate(BaseModel):
    round_name: str = Field(min_length=1, max_length=100)
    scheduled_at: datetime | None = None
    status: Literal[
        "Scheduled",
        "Completed",
        "Cancelled"
    ] = "Scheduled"
    notes: str | None = None


class InterviewUpdate(BaseModel):
    round_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    scheduled_at: datetime | None = None
    status: Literal[
        "Scheduled",
        "Completed",
        "Cancelled"
    ] | None = None
    notes: str | None = None


class InterviewResponse(BaseModel):
    id: str
    application_id: str
    round_name: str
    scheduled_at: datetime | None
    status: str
    notes: str | None

    model_config = ConfigDict(from_attributes=True)
