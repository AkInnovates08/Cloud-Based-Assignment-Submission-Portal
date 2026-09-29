from functools import lru_cache
from app.core.config import settings

@lru_cache
def get_client():
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase URL/service-role key are not configured")
    from supabase import create_client
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

def get_verified_user(access_token: str):
    client = get_client()
    response = client.auth.get_user(access_token)
    return response.user
