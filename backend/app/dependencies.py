from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.core.config import settings
from app.models.models import User

bearer = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    token = credentials.credentials

    if settings.AUTH_MODE.lower() == "supabase":
        try:
            from app.services.supabase import get_verified_user
            remote = get_verified_user(token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid Supabase access token")
        user = db.query(User).filter(User.external_auth_id == remote.id).first()
        if not user:
            raise HTTPException(status_code=403, detail="Cloud auth user has no application profile")
        return user

    payload = decode_token(token)
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(*roles):
    def checker(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker
