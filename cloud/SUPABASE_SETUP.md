# Supabase Cloud Authentication + Storage Setup

This project supports a `local` mode and a `supabase` mode.

## 1. Create project
Create a Supabase project and enable email/password authentication.

## 2. Create private bucket
Create a private Storage bucket named `assignments`.

The backend uses the service-role key only server-side for storage operations. Never place it in React or GitHub.

## 3. Database
Run `cloud/supabase_schema.sql` in the SQL Editor.

## 4. Backend environment
Set:
```text
AUTH_MODE=supabase
STORAGE_BACKEND=supabase
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVER_ONLY_SECRET
SUPABASE_STORAGE_BUCKET=assignments
SUPABASE_TEACHER_EMAILS=approved-teacher@example.com
DATABASE_URL=postgresql+psycopg2://...
```

The teacher allowlist is deliberate: role selection must not be freely trusted from a public browser.

## 5. How authentication works
The frontend obtains a Supabase Auth access token. It sends that token as:
```text
Authorization: Bearer <access-token>
```

FastAPI verifies the token through Supabase Auth and maps the verified Supabase user ID (`sub`) to the application's `users.external_auth_id`.

Supabase documents JWT verification using its project's JWKS endpoint and also provides Python client methods for verified user claims.

## 6. Create application profile
After Supabase signup/login, call:
```http
POST /api/auth/cloud-profile?name=Student%20One&role=student
Authorization: Bearer <supabase-access-token>
```

Teacher creation succeeds only when the email is in `SUPABASE_TEACHER_EMAILS`.

## 7. Storage path
Files are stored as:
```text
assignments/assignment_<id>/student_<id>/<timestamp>_<filename>
```

Keep the bucket private. For a larger production system, prefer short-lived signed URLs/direct-to-storage uploads so the API does not proxy large files.

## 8. Local mode remains reproducible
For an offline classroom demo:
```text
AUTH_MODE=local
STORAGE_BACKEND=local
DATABASE_URL=sqlite:///./assignment_portal.db
```

This is intentionally the default.
