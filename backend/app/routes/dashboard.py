from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import require_role
from app.models.models import Assignment, Submission, User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/student")
def student_dashboard(db: Session = Depends(get_db), student=Depends(require_role("student"))):
    assignments = db.query(Assignment).count()
    mine = db.query(Submission).filter(Submission.student_id == student.id).all()
    return {
        "student": student.name,
        "total_assignments": assignments,
        "submitted": sum(1 for s in mine if s.submission_status in ("SUBMITTED","GRADED")),
        "late": sum(1 for s in mine if s.submission_status == "LATE"),
        "graded": sum(1 for s in mine if s.submission_status == "GRADED"),
        "pending": max(assignments - len(mine), 0),
        "recent_feedback": [
            {"submission_id": s.id, "marks": s.marks, "feedback": s.feedback}
            for s in mine if s.feedback
        ][:5]
    }

@router.get("/teacher")
def teacher_dashboard(db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    assignment_ids = [a.id for a in db.query(Assignment).filter(Assignment.created_by == teacher.id).all()]
    submissions = db.query(Submission).filter(Submission.assignment_id.in_(assignment_ids)).all() if assignment_ids else []
    students = db.query(User).filter(User.role == "student").count()
    return {
        "teacher": teacher.name,
        "total_assignments": len(assignment_ids),
        "total_students": students,
        "total_submissions": len(submissions),
        "pending_reviews": sum(1 for s in submissions if s.submission_status != "GRADED"),
        "late_submissions": sum(1 for s in submissions if s.submission_status == "LATE"),
        "graded_submissions": sum(1 for s in submissions if s.submission_status == "GRADED"),
    }
