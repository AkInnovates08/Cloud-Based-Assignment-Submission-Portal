# Interview Preparation

## 1. Explain your project.
**Answer:** My project is a Cloud-Based Student Assignment Submission and Feedback Portal. Teachers create assignments with deadlines and file rules. Students authenticate, view assignments, upload their work, and later see marks and feedback. The important cloud concept is separation of concerns: structured metadata is stored in a relational database while assignment files are stored in object storage. The API enforces authentication and role-based authorization, and the application can move from local SQLite/local storage to managed PostgreSQL/object storage without changing the core workflow.

## 2. Why did you use object storage instead of database BLOBs?
**Answer:** Assignment files are binary objects and can be much larger than normal records. Object storage is designed for this workload, while the database stores metadata such as filename, storage path, submission time, status, marks and feedback. This reduces database size and allows file storage to scale independently.

## 3. What is the difference between authentication and authorization?
**Answer:** Authentication answers who the user is. Authorization answers what that authenticated user is allowed to do. In this project a token identifies the user and the API checks the user's role before sensitive operations.

## 4. How is RBAC implemented?
**Answer:** The user has a server-side role such as student or teacher. Protected endpoints use dependency checks. A student can submit and view their own work, while a teacher can create assignments and grade submissions belonging to their courses.

## 5. How does the deadline work?
**Answer:** The backend compares the server-side submission timestamp with the assignment deadline. If the timestamp is before or equal to the deadline the status is SUBMITTED; otherwise it is LATE. This avoids trusting the student's computer clock.

## 6. How would you deploy it to the cloud?
**Answer:** I would host the React frontend as a static site, deploy FastAPI as a web service, use managed PostgreSQL for metadata, a managed object-storage bucket for files, and a managed authentication service such as Supabase Auth. HTTPS and environment-managed secrets would be enabled.

## 7. How would you scale 100,000 deadline submissions?
**Answer:** I would keep the API stateless, use a load balancer/autoscaling, use direct-to-object-storage uploads with short-lived signed permissions, use managed PostgreSQL with pooling and indexes, and move virus scanning and notifications to a queue and background workers. A CDN would serve frontend assets.

## 8. What security controls did you consider?
**Answer:** Password hashing, expiring JWTs, RBAC, server-side validation, private files, controlled file paths, HTTPS, environment variables, CORS, rate limiting, logging and audit trails. In a production cloud version I would also add malware scanning and signed URLs.

## 9. What happens if storage succeeds but the database write fails?
**Answer:** The workflow needs compensation. The system can delete the orphaned object or put it into a quarantine/pending area and retry the metadata transaction. An idempotency key prevents duplicate logical submissions.

## 10. What is the difference between local and cloud deployment?
**Answer:** Local mode uses SQLite, local disk and application-managed JWT authentication for learning and testing. Cloud mode replaces those components with managed PostgreSQL, private object storage and managed authentication. The application architecture stays service-oriented, so the deployment environment changes without changing the core user workflow.
