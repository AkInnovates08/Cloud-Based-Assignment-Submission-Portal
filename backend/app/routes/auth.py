from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from app.dependencies import bearer
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.schemas import UserCreate, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(
        name=data.name.strip(),
        email=data.email.lower(),
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(str(user.id), user.role)
    return {"access_token": token, "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(str(user.id), user.role)
    return {"access_token": token, "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}


@router.post("/cloud-profile")
def create_cloud_profile(
    name: str,
    role: str,
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    if settings.AUTH_MODE.lower() != "supabase":
        raise HTTPException(status_code=400, detail="Cloud authentication mode is disabled")
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    try:
        from app.services.supabase import get_verified_user
        remote = get_verified_user(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Supabase access token")

    email = (remote.email or "").lower()
    role = role.lower()
    if role not in {"student", "teacher"}:
        raise HTTPException(status_code=400, detail="Role must be student or teacher")
    # For a student project, teacher creation is restricted to a server-side allowlist.
    if role == "teacher" and email not in settings.SUPABASE_TEACHER_EMAILS:
        raise HTTPException(status_code=403, detail="Teacher role requires an approved email")

    existing = db.query(User).filter(User.external_auth_id == remote.id).first()
    if existing:
        return {"id": existing.id, "name": existing.name, "email": existing.email, "role": existing.role}

    user = User(name=name.strip(), email=email, role=role, external_auth_id=remote.id, password_hash="SUPABASE_MANAGED")
    db.add(user); db.commit(); db.refresh(user)
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

@router.post("/logout")
def logout(user=Depends(get_current_user)):
    # JWTs are stateless; frontend removes the token.
    return {"message": "Logged out on client; token expires according to server policy."}
