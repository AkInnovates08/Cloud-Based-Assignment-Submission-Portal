from pathlib import Path
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.models import Assignment, Submission, Course
from app.schemas.schemas import GradeRequest
from app.services.storage import storage, validate_upload

router = APIRouter(tags=["Submissions"])

def normalize_dt(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

@router.post("/assignments/{assignment_id}/submit", status_code=201)
def submit_assignment(
    assignment_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    student=Depends(require_role("student")),
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment: raise HTTPException(status_code=404, detail="Assignment not found")
    validate_upload(file, assignment.allowed_file_types, assignment.max_file_size_mb)

    content = file.file.read()
    if len(content) > assignment.max_file_size_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds maximum allowed size")
    file.file.seek(0)

    existing = db.query(Submission).filter(
        Submission.assignment_id == assignment_id,
        Submission.student_id == student.id
    ).first()

    if existing:
        return _resubmit(existing, assignment, file, db)

    now = datetime.now(timezone.utc)
    status = "SUBMITTED" if now <= normalize_dt(assignment.deadline) else "LATE"
    path = f"assignments/assignment_{assignment.id}/student_{student.id}/{now.strftime('%Y%m%d%H%M%S')}_{Path(file.filename).name}"
    stored = storage.save(file, path)
    submission = Submission(
        assignment_id=assignment.id, student_id=student.id, file_name=file.filename,
        storage_path=stored, file_url=None, submitted_at=now, submission_status=status
    )
    db.add(submission); db.commit(); db.refresh(submission)
    return _serialize(submission)

def _resubmit(existing, assignment, file, db):
    now = datetime.now(timezone.utc)
    path = f"assignments/assignment_{assignment.id}/student_{existing.student_id}/{now.strftime('%Y%m%d%H%M%S')}_{Path(file.filename).name}"
    stored = storage.save(file, path)
    existing.file_name = file.filename
    existing.storage_path = stored
    existing.submitted_at = now
    existing.submission_status = "SUBMITTED" if now <= normalize_dt(assignment.deadline) else "LATE"
    existing.marks = None
    existing.feedback = None
    existing.graded_at = None
    db.commit(); db.refresh(existing)
    return _serialize(existing)

def _serialize(s):
    return {
        "id": s.id, "assignment_id": s.assignment_id, "student_id": s.student_id,
        "file_name": s.file_name, "storage_path": s.storage_path,
        "submitted_at": s.submitted_at, "submission_status": s.submission_status,
        "marks": s.marks, "feedback": s.feedback, "graded_at": s.graded_at
    }

@router.get("/submissions/me")
def my_submissions(db: Session = Depends(get_db), student=Depends(require_role("student"))):
    return [_serialize(s) for s in db.query(Submission).filter(Submission.student_id == student.id).order_by(Submission.submitted_at.desc()).all()]

@router.get("/assignments/{assignment_id}/submissions")
def assignment_submissions(assignment_id: int, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id, Assignment.created_by == teacher.id).first()
    if not assignment: raise HTTPException(status_code=404, detail="Assignment not found")
    return [_serialize(s) for s in db.query(Submission).filter(Submission.assignment_id == assignment_id).order_by(Submission.submitted_at.desc()).all()]

@router.get("/submissions/{submission_id}")
def get_submission(submission_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    s = db.query(Submission).filter(Submission.id == submission_id).first()
    if not s: raise HTTPException(status_code=404, detail="Submission not found")
    if user.role == "student" and s.student_id != user.id: raise HTTPException(status_code=403, detail="Forbidden")
    if user.role == "teacher" and s.assignment.created_by != user.id: raise HTTPException(status_code=403, detail="Forbidden")
    return _serialize(s)

@router.get("/submissions/{submission_id}/download")
def download_submission(submission_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    s = db.query(Submission).filter(Submission.id == submission_id).first()
    if not s: raise HTTPException(status_code=404, detail="Submission not found")
    if user.role == "student" and s.student_id != user.id: raise HTTPException(status_code=403, detail="Forbidden")
    if user.role == "teacher" and s.assignment.created_by != user.id: raise HTTPException(status_code=403, detail="Forbidden")
    path = storage.open(s.storage_path)
    return FileResponse(path, filename=s.file_name, media_type="application/octet-stream")

@router.post("/submissions/{submission_id}/grade")
def grade_submission(submission_id: int, data: GradeRequest, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    s = db.query(Submission).filter(Submission.id == submission_id).first()
    if not s or s.assignment.created_by != teacher.id: raise HTTPException(status_code=404, detail="Submission not found")
    if data.marks > s.assignment.max_marks:
        raise HTTPException(status_code=400, detail=f"Marks cannot exceed {s.assignment.max_marks}")
    s.marks = data.marks
    s.feedback = data.feedback.strip()
    s.graded_at = datetime.now(timezone.utc)
    s.submission_status = "GRADED"
    db.commit(); db.refresh(s)
    return _serialize(s)

@router.get("/submissions/{submission_id}/feedback")
def get_feedback(submission_id: int, db: Session = Depends(get_db), student=Depends(require_role("student"))):
    s = db.query(Submission).filter(Submission.id == submission_id, Submission.student_id == student.id).first()
    if not s: raise HTTPException(status_code=404, detail="Submission not found")
    return {"marks": s.marks, "feedback": s.feedback, "graded_at": s.graded_at}
