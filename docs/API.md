# REST API

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | `/api/auth/register` | Public | Register |
| POST | `/api/auth/login` | Public | Login |
| POST | `/api/auth/logout` | Auth | Logout acknowledgement |
| GET | `/api/auth/me` | Auth | Current user |
| POST | `/api/courses` | Teacher | Create course |
| GET | `/api/courses` | Auth | List courses |
| POST | `/api/assignments` | Teacher | Create assignment |
| GET | `/api/assignments` | Auth | List assignments |
| GET | `/api/assignments/{id}` | Auth | Assignment details |
| PUT | `/api/assignments/{id}` | Teacher owner | Update |
| DELETE | `/api/assignments/{id}` | Teacher owner | Delete |
| POST | `/api/assignments/{id}/submit` | Student | Upload/resubmit |
| GET | `/api/submissions/me` | Student | Own submissions |
| GET | `/api/assignments/{id}/submissions` | Teacher owner | Review submissions |
| GET | `/api/submissions/{id}` | Owner/teacher | Submission details |
| GET | `/api/submissions/{id}/download` | Owner/teacher | Download file |
| POST | `/api/submissions/{id}/grade` | Teacher owner | Grade |
| GET | `/api/submissions/{id}/feedback` | Student owner | Feedback |
| GET | `/api/dashboard/student` | Student | Student metrics |
| GET | `/api/dashboard/teacher` | Teacher | Teacher metrics |
| GET | `/api/health` | Public | Health check |

Expected status codes: 200 success, 201 created, 400 validation/business rule failure, 401 unauthenticated, 403 unauthorized, 404 missing resource, 409 conflict, 413 oversized file, 500 unexpected server error, 503 temporary dependency failure.
