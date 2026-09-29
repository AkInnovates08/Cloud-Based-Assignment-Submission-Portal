# System Architecture

## Recommended student-friendly architecture

```text
 Student / Teacher
        |
        v
 React Web Application
        |
        v
 FastAPI REST API
        |
   +----+----------------+
   |                     |
   v                     v
PostgreSQL/SQLite    Object Storage
(metadata)           (PDF/DOCX/etc.)
   |
   v
Feedback + Marks
```

Cloud deployment adds:

```text
Users
  |
CDN / Static Hosting
  |
React Frontend
  |
API Gateway / HTTPS
  |
FastAPI Backend
  |
+-----------------------------+
| Managed PostgreSQL          |
| Private Object Storage      |
| Authentication              |
| Logging / Monitoring        |
+-----------------------------+
```

## Request flow

1. User authenticates.
2. Frontend stores the short-lived access token.
3. Protected API calls include `Authorization: Bearer <token>`.
4. FastAPI validates the token and role.
5. Metadata is stored in a relational database.
6. Assignment files are stored separately in object storage.
7. Teacher reads a submission only when authorized.
8. Marks and feedback are written to the database.
9. Student reads only their own feedback.

## Why separate DB and object storage?

Relational databases are optimized for structured records and queries. Object storage is optimized for large binary objects. Keeping only a storage reference in the database reduces database bloat and makes file storage independently scalable.
