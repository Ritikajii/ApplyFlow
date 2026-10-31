


from sqlalchemy import Column, String, Date, ForeignKey,Text,DateTime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)


class Application(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    application_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="Applied")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String, primary_key=True, index=True)

    application_id = Column(
        String,
        ForeignKey("applications.id"),
        nullable=False,
        index=True
    )

    round_name = Column(String(100), nullable=False)

    scheduled_at = Column(DateTime(timezone=True), nullable=True)

    status = Column(
        String(20),
        nullable=False,
        default="Scheduled"
    )

    notes = Column(Text, nullable=True)
