# Cloud-Based Student Assignment Submission & Feedback Portal

## Abstract
This project implements a cloud-oriented portal for assignment creation, submission, review, grading and feedback. It separates structured metadata from binary assignment files and uses authentication and role-based authorization to protect student and teacher workflows.

## Introduction
Traditional assignment handling often depends on email, shared folders and manual tracking. A centralized web portal provides one workflow for deadlines, submissions, marks and feedback.

## Problem Statement
Students need a reliable way to access coursework and submit files remotely. Teachers need centralized visibility of submissions and a controlled mechanism for grading and feedback.

## Objectives
- Provide student and teacher authentication.
- Implement role-based access control.
- Manage courses and assignments.
- Store submission metadata in a database.
- Store files in object storage.
- Implement deadline and resubmission logic.
- Provide grading and feedback.
- Demonstrate cloud deployment, security and scalability.

## Existing System
Email attachments, local folders or ad-hoc shared drives can make status tracking and access control difficult.

## Proposed System
A web application backed by a REST API, managed database, object storage and authentication service.

## User Roles
Students submit work and view their own status/feedback. Teachers create assignments and grade submissions.

## Cloud Computing Concepts
The system demonstrates SaaS, PaaS, managed databases, object storage, authentication, RBAC, REST APIs, serverless mapping, scalability, availability, CDN, API gateways, secrets, logging, monitoring, backup and CI/CD.

## Technology Stack
React, FastAPI, SQLAlchemy, SQLite for local simulation, PostgreSQL for cloud deployment, and private object storage.

## Architecture
See `ARCHITECTURE.md`.

## Database Design
Users, courses, assignments and submissions are normalized relational records. Indexes support role, deadline, assignment and student queries.

## Cloud Storage Design
Files are stored outside the relational database. The database stores a controlled storage path/reference.

## Authentication
Local mode uses bcrypt passwords and expiring JWTs. The cloud architecture can use Supabase Auth or another managed identity service.

## Assignment Management
Teachers create, update and delete assignments and configure deadline, maximum marks, allowed types and maximum file size.

## Submission Workflow
The student selects an assignment, the API validates the user and file, stores the file, and records metadata.

## Deadline Management
The server uses its own timestamp and compares it to the assignment deadline. Client time is not trusted.

## Feedback & Grading
Teachers can grade only submissions belonging to their assignments. Marks are validated against maximum marks.

## API Design
See `API.md`.

## Implementation
The implementation is split into frontend, backend, models, services, tests and cloud configuration.

## Testing
Automated tests cover registration, login, authorization, assignment creation, upload, grading and mark validation. Manual tests are listed in `TEST_PLAN.md`.

## Cloud Deployment
A student-friendly path is React static hosting plus a FastAPI web service plus Supabase for Postgres/Auth/Storage. An AWS mapping is included in the main README.

## Security
HTTPS, private storage, signed URLs, RBAC, password hashing, environment variables, validation, rate limiting, logging and audit trails are recommended.

## Scalability
Stateless APIs, managed databases, object storage, CDN, caching, queues and autoscaling allow the architecture to grow beyond a classroom prototype.

## Results
The completed system demonstrates a complete assignment lifecycle from authentication through submission to grading and feedback.

## Advantages
Centralized workflow, remote access, searchable metadata, scalable files, role separation and auditable grading.

## Limitations
The local mode is a simulation and is not suitable for production. Malware scanning, signed cloud URLs and advanced monitoring require additional deployment configuration.

## Future Scope
Notifications, plagiarism checking, virus scanning, analytics, calendar integration, SSO, mobile application, background processing and richer audit trails.

## Conclusion
The project demonstrates that cloud computing is more than hosting a website: it separates application compute, authentication, structured data and file storage into services that can scale independently.
