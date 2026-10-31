

from fastapi import FastAPI, HTTPException, Depends,Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Literal
from app.models import User
from app.schemas import UserRegister
from app.security import hash_password
from app.database import get_db,SessionLocal
from app.schemas import UserLogin, TokenResponse
from app.security import verify_password
from app.auth import create_access_token
from app.models import Application
from app.models import Interview
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.schemas import InterviewCreate, InterviewResponse
from app.schemas import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
)
from app.schemas import InterviewUpdate
from app.dependencies import get_current_user
app = FastAPI(title="ApplyFlow API")


@app.get("/")
def home():
    return {"message": "Welcome to ApplyFlow API"}


@app.post(
    "/applications",
    status_code=201,
    response_model=ApplicationResponse
)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_application = Application(
        id=str(uuid4()),
        user_id=current_user.id,
        **application.model_dump()
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

@app.get("/applications", response_model=list[ApplicationResponse])
def get_applications(
    status: Literal["Applied", "Interview", "Offer", "Rejected"] | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Application).filter(
        Application.user_id == current_user.id
    )

    if status is not None:
        query = query.filter(Application.status == status)

    return query.offset(skip).limit(limit).all()



@app.get(
    "/applications/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application



@app.delete("/applications/{application_id}")
def delete_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return {"message": "Application deleted successfully"}


@app.patch(
    "/applications/{application_id}",
    response_model=ApplicationResponse
)
def update_application(
    application_id: str,
    updates: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    update_data = updates.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)

    return application




@app.post("/auth/register", status_code=201)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    new_user = User(
        id=str(uuid4()),
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }

@app.post("/auth/login", response_model=TokenResponse)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == credentials.email)
        .first()
    )

    if user is None or not verify_password(
        credentials.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post(
    "/applications/{application_id}/interviews",
    status_code=201,
    response_model=InterviewResponse
)
def create_interview(
    application_id: str,
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    new_interview = Interview(
        id=str(uuid4()),
        application_id=application_id,
        **interview.model_dump()
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return new_interview

@app.get(
    "/applications/{application_id}/interviews",
    response_model=list[InterviewResponse]
)
def get_interviews(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    interviews = db.query(Interview).filter(
        Interview.application_id == application_id
    ).all()

    return interviews

@app.patch(
    "/interviews/{interview_id}",
    response_model=InterviewResponse
)
def update_interview(
    interview_id: str,
    updates: InterviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interview = db.query(Interview).join(Application).filter(
        Interview.id == interview_id,
        Application.user_id == current_user.id
    ).first()

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    update_data = updates.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(interview, key, value)

    db.commit()
    db.refresh(interview)

    return interview

@app.delete("/interviews/{interview_id}")
def delete_interview(
    interview_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interview = db.query(Interview).join(Application).filter(
        Interview.id == interview_id,
        Application.user_id == current_user.id
    ).first()

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    db.delete(interview)
    db.commit()

    return {"message": "Interview deleted successfully"}

@app.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Application).filter(
        Application.user_id == current_user.id
    ).count()

    applied = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.status == "Applied"
    ).count()

    interviews = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.status == "Interview"
    ).count()

    offers = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.status == "Offer"
    ).count()

    rejected = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.status == "Rejected"
    ).count()

    total_interview_rounds = db.query(Interview).join(
        Application
    ).filter(
        Application.user_id == current_user.id
    ).count()

    offer_rate = round((offers / total) * 100, 2) if total > 0 else 0

    return {
        "total_applications": total,
        "applied": applied,
        "in_interview": interviews,
        "offers": offers,
        "rejected": rejected,
        "total_interview_rounds": total_interview_rounds,
        "offer_rate_percentage": offer_rate
    }

@app.get(
    "/reminders/upcoming",
    response_model=list[InterviewResponse]
)
def get_upcoming_reminders(
    days: int = Query(default=7, ge=1, le=30),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.now(timezone.utc)
    reminder_deadline = now + timedelta(days=days)

    upcoming = db.query(Interview).join(Application).filter(
        Application.user_id == current_user.id,
        Interview.status == "Scheduled",
        Interview.scheduled_at >= now,
        Interview.scheduled_at <= reminder_deadline
    ).order_by(Interview.scheduled_at.asc()).all()

    return upcoming
