import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings:
    APP_NAME = os.getenv("APP_NAME", "Cloud Assignment Portal")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'assignment_portal.db'}")
    STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")
    AUTH_MODE = os.getenv("AUTH_MODE", "local")
    STORAGE_DIR = Path(os.getenv("STORAGE_DIR", str(BASE_DIR / "storage")))
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_EXTENSIONS = {
        x.strip().lower().lstrip(".")
        for x in os.getenv("ALLOWED_EXTENSIONS", "pdf,docx,txt,png,jpg,jpeg,zip").split(",")
        if x.strip()
    }
    CORS_ORIGINS = [x.strip() for x in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",") if x.strip()]

    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "assignments")
    SUPABASE_TEACHER_EMAILS = {x.strip().lower() for x in os.getenv("SUPABASE_TEACHER_EMAILS", "").split(",") if x.strip()}

settings = Settings()
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
