from pathlib import Path
import shutil
from fastapi import UploadFile, HTTPException
from app.core.config import settings

class LocalStorage:
    def save(self, upload: UploadFile, path: str) -> str:
        target = settings.STORAGE_DIR / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("wb") as out:
            shutil.copyfileobj(upload.file, out)
        return str(target.relative_to(settings.STORAGE_DIR))

    def open(self, path: str):
        target = settings.STORAGE_DIR / path
        if not target.exists() or not target.is_file():
            raise HTTPException(status_code=404, detail="Stored file not found")
        return target

    def delete(self, path: str):
        target = settings.STORAGE_DIR / path
        if target.exists():
            target.unlink()

class SupabaseStorage:
    def save(self, upload: UploadFile, path: str) -> str:
        try:
            from app.services.supabase import get_client
            client = get_client()
            data = upload.file.read()
            client.storage.from_(settings.SUPABASE_STORAGE_BUCKET).upload(
                path=path,
                file=data,
                file_options={"upsert": "false", "content-type": upload.content_type or "application/octet-stream"}
            )
            return path
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Cloud storage upload failed: {exc}")

    def open(self, path: str):
        # For private buckets, download through the trusted backend.
        try:
            from app.services.supabase import get_client
            data = get_client().storage.from_(settings.SUPABASE_STORAGE_BUCKET).download(path)
            tmp = settings.STORAGE_DIR / "tmp_downloads" / Path(path).name
            tmp.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_bytes(data)
            return tmp
        except Exception as exc:
            raise HTTPException(status_code=404, detail=f"Cloud file unavailable: {exc}")

    def delete(self, path: str):
        from app.services.supabase import get_client
        get_client().storage.from_(settings.SUPABASE_STORAGE_BUCKET).remove([path])

storage = SupabaseStorage() if settings.STORAGE_BACKEND.lower() == "supabase" else LocalStorage()

def validate_upload(upload: UploadFile, allowed: str, max_mb: int):
    filename = upload.filename or ""
    ext = Path(filename).suffix.lower().lstrip(".")
    allowed_set = {x.strip().lower().lstrip(".") for x in allowed.split(",") if x.strip()}
    if ext not in allowed_set:
        raise HTTPException(status_code=400, detail=f"File type .{ext} is not allowed")
    if not filename or len(filename) > 255:
        raise HTTPException(status_code=400, detail="Invalid file name")
    return ext
