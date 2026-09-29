from datetime import datetime, timezone
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    external_auth_id: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), index=True, default="student")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_name: Mapped[str] = mapped_column(String(150), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    teacher = relationship("User")

class Assignment(Base):
    __tablename__ = "assignments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    max_marks: Mapped[int] = mapped_column(Integer, nullable=False)
    allowed_file_types: Mapped[str] = mapped_column(String(300), default="pdf,docx,txt")
    max_file_size_mb: Mapped[int] = mapped_column(Integer, default=10)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    course = relationship("Course")
    creator = relationship("User")

class Submission(Base):
    __tablename__ = "submissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"), nullable=False, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    submission_status: Mapped[str] = mapped_column(String(30), default="SUBMITTED", index=True)
    marks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    graded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    assignment = relationship("Assignment")
    student = relationship("User")

Index("ix_submission_assignment_student", Submission.assignment_id, Submission.student_id)
