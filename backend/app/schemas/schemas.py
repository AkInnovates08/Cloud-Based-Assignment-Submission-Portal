from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(pattern="^(student|teacher)$")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class CourseCreate(BaseModel):
    course_name: str = Field(min_length=2, max_length=150)

class AssignmentCreate(BaseModel):
    course_id: int
    title: str = Field(min_length=2, max_length=200)
    description: str = ""
    deadline: datetime
    max_marks: int = Field(gt=0, le=1000)
    allowed_file_types: str = "pdf,docx,txt"
    max_file_size_mb: int = Field(gt=0, le=100)

class AssignmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course_id: int
    title: str
    description: str
    deadline: datetime
    max_marks: int
    allowed_file_types: str
    max_file_size_mb: int

class GradeRequest(BaseModel):
    marks: int = Field(ge=0)
    feedback: str = Field(default="", max_length=5000)
