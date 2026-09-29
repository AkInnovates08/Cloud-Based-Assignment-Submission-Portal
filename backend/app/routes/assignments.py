from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import require_role, get_current_user
from app.models.models import Assignment, Course, User
from app.schemas.schemas import AssignmentCreate, AssignmentOut, CourseCreate

router = APIRouter(tags=["Assignments"])

@router.post("/courses", status_code=201)
def create_course(data: CourseCreate, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    course = Course(course_name=data.course_name.strip(), teacher_id=teacher.id)
    db.add(course); db.commit(); db.refresh(course)
    return {"id": course.id, "course_name": course.course_name, "teacher_id": course.teacher_id}

@router.get("/courses")
def get_courses(db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(Course)
    if user.role == "teacher":
        q = q.filter(Course.teacher_id == user.id)
    return q.order_by(Course.id.desc()).all()


@router.get("/teachers")
def get_teachers(db: Session = Depends(get_db), user=Depends(get_current_user)):
    teachers = db.query(User).filter(User.role == "teacher").order_by(User.name.asc()).all()
    return [{"id": t.id, "name": t.name, "email": t.email, "role": t.role} for t in teachers]

@router.post("/assignments", response_model=AssignmentOut, status_code=201)
def create_assignment(data: AssignmentCreate, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    course = db.query(Course).filter(Course.id == data.course_id, Course.teacher_id == teacher.id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not owned by teacher")
    assignment = Assignment(**data.model_dump(), created_by=teacher.id)
    db.add(assignment); db.commit(); db.refresh(assignment)
    return assignment

@router.get("/assignments", response_model=list[AssignmentOut])
def get_assignments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Assignment).order_by(Assignment.deadline.asc()).all()

@router.get("/assignments/{assignment_id}", response_model=AssignmentOut)
def get_assignment(assignment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not item: raise HTTPException(status_code=404, detail="Assignment not found")
    return item

@router.put("/assignments/{assignment_id}", response_model=AssignmentOut)
def update_assignment(assignment_id: int, data: AssignmentCreate, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    item = db.query(Assignment).filter(Assignment.id == assignment_id, Assignment.created_by == teacher.id).first()
    if not item: raise HTTPException(status_code=404, detail="Assignment not found")
    course = db.query(Course).filter(Course.id == data.course_id, Course.teacher_id == teacher.id).first()
    if not course: raise HTTPException(status_code=404, detail="Course not found")
    for key, value in data.model_dump().items(): setattr(item, key, value)
    db.commit(); db.refresh(item)
    return item

@router.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db), teacher=Depends(require_role("teacher"))):
    item = db.query(Assignment).filter(Assignment.id == assignment_id, Assignment.created_by == teacher.id).first()
    if not item: raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(item); db.commit()
    return {"message": "Assignment deleted"}
