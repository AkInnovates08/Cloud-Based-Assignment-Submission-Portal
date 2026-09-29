# Cloud-Based Student Assignment Submission & Feedback Portal

A full-stack cloud-oriented web application for managing student assignments, submissions, grading, feedback, courses, and teacher workflows.

The system provides separate student and teacher experiences with authentication, role-based access control, assignment management, file upload and resubmission, deadline tracking, grading, feedback, and cloud-ready storage/database architecture.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Key Features](#key-features)
* [User Roles](#user-roles)
* [Application Workflow](#application-workflow)
* [Technology Stack](#technology-stack)
* [System Architecture](#system-architecture)
* [Project Structure](#project-structure)
* [Database Design](#database-design)
* [Assignment and Submission Workflow](#assignment-and-submission-workflow)
* [Authentication and Authorization](#authentication-and-authorization)
* [File Storage](#file-storage)
* [Frontend](#frontend)
* [Backend API](#backend-api)
* [Local Development Setup](#local-development-setup)
* [Environment Configuration](#environment-configuration)
* [Running the Application](#running-the-application)
* [Creating a Teacher Course](#creating-a-teacher-course)
* [Testing](#testing)
* [API Documentation](#api-documentation)
* [Cloud Deployment](#cloud-deployment)
* [Security](#security)
* [Scalability](#scalability)
* [Failure Handling](#failure-handling)
* [Future Enhancements](#future-enhancements)
* [Project Documentation](#project-documentation)
* [Learning Outcomes](#learning-outcomes)
* [Project Use Case](#project-use-case)
* [Resume Description](#resume-description)
* [Author](#author)

---

## Project Overview

The Cloud-Based Student Assignment Submission & Feedback Portal is designed to demonstrate how a real-world academic assignment management platform can be built using modern full-stack and cloud computing concepts.

The application allows:

### Students

* Register and log in securely
* View available assignments
* View assignment deadlines
* View course information
* Upload assignment files
* Resubmit assignments when permitted
* Track submission status
* View marks
* View teacher feedback
* Access their submitted files

### Teachers

* Register and log in
* Create and manage courses
* Create assignments
* Update assignments
* Delete assignments
* Configure deadlines
* Define maximum marks
* Configure allowed file types
* Configure maximum upload size
* View student submissions
* Download submitted files
* Grade assignments
* Provide feedback
* Monitor assignment activity

The project is designed with a cloud-ready architecture so that local development can later be migrated to managed cloud services such as Supabase, AWS, Azure, or Google Cloud.

---

## Key Features

### Authentication

* Student and teacher registration
* Secure login
* Password hashing
* JWT-based authentication
* Protected API endpoints
* Session/token validation

### Role-Based Access Control

The system provides different capabilities based on the authenticated user's role.

| Role    | Capabilities                                                                                           |
| ------- | ------------------------------------------------------------------------------------------------------ |
| Student | View assignments, upload submissions, resubmit work, view marks and feedback                           |
| Teacher | Manage courses, create assignments, manage assignments, review submissions, grade and provide feedback |

---

## Student Features

### Student Dashboard

Students can access an overview of their academic assignment activity.

The dashboard provides information such as:

* Available assignments
* Submission activity
* Pending assignments
* Graded assignments
* Submission status

### Assignment Discovery

Students can:

* Browse assignments
* Search assignments
* View assignment descriptions
* View deadlines
* View maximum marks
* View allowed file types
* View maximum file size

### Assignment Submission

Students can upload supported files according to the assignment configuration.

Example supported formats:

```text
PDF
DOCX
TXT
PNG
JPG
JPEG
ZIP
```

### Resubmission

The system supports resubmission according to the configured assignment rules.

### Submission Status

Submissions can have statuses such as:

```text
NOT_SUBMITTED
SUBMITTED
LATE
GRADED
```

### Feedback

Students can view:

* Marks received
* Teacher feedback
* Submission status

---

## Teacher Features

### Teacher Dashboard

Teachers receive an overview of their assignment management activities.

### Course Management

Teachers can create courses before creating assignments.

Example:

```text
Cloud Computing
Artificial Intelligence
Database Management
Web Development
Software Engineering
```

When a teacher creates an assignment, the available courses appear in the course selection dropdown.

### Creating a Course

From the assignment creation interface:

```text
Assignments
    |
    +-- New Assignment
            |
            +-- New Course
                    |
                    +-- Enter Course Name
                    |
                    +-- Create Course
```

The newly created course is automatically added to the course selection list.

### Assignment Management

Teachers can:

* Create assignments
* Update assignments
* Delete assignments
* Select courses
* Set deadlines
* Set maximum marks
* Configure file extensions
* Configure upload size limits

Example assignment:

```text
Course:
Cloud Computing

Assignment:
Cloud Deployment Architecture

Maximum Marks:
100

Deadline:
2026-10-15

Allowed Files:
pdf,docx,png

Maximum File Size:
10 MB
```

### Submission Review

Teachers can:

* View student submissions
* Review submission status
* Download submission files
* Grade submissions
* Add feedback

---

# Application Workflow

The overall workflow is:

```text
                    Cloud Assignment Portal
                              |
                +-------------+-------------+
                |                           |
             Student                     Teacher
                |                           |
             Register                    Register
                |                           |
              Login                       Login
                |                           |
          Student Dashboard          Teacher Dashboard
                |                           |
          View Assignments          Manage Courses
                |                           |
          Select Assignment         Create Assignment
                |                           |
          Upload Submission         View Submissions
                |                           |
          Track Status              Grade Submission
                |                           |
          View Marks                Add Feedback
                |                           |
          View Feedback                    |
```

---

# Technology Stack

## Frontend

* React
* Vite
* JavaScript
* Axios
* HTML5
* CSS3

## Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic
* JWT Authentication
* Passlib / bcrypt

## Database

### Local Development

* SQLite

### Cloud-Ready

* PostgreSQL
* Supabase PostgreSQL

## Storage

### Local Development

* Local filesystem storage

### Cloud

* Supabase Storage
* AWS S3
* Azure Blob Storage
* Google Cloud Storage

## Deployment

The project can be deployed using:

* Render
* Supabase
* AWS
* Microsoft Azure
* Google Cloud Platform

---

# System Architecture

```text
                         User
                          |
             +------------+------------+
             |                         |
          Student                    Teacher
             |                         |
             +------------+------------+
                          |
                       React
                       Frontend
                          |
                       Axios
                          |
                       REST API
                          |
                      FastAPI
                       Backend
                          |
             +------------+-------------+
             |                          |
        Authentication              Business Logic
             |                          |
             +------------+-------------+
                          |
              +-----------+-----------+
              |                       |
          PostgreSQL              Object Storage
          / SQLite               / Supabase Storage
              |                       |
          User Data              Assignment Files
          Courses                Submission Files
          Assignments
          Submissions
```

---

# Project Structure

```text
Cloud-Based-Assignment-Submission-Portal/
│
├── backend/
│   │
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── course.py
│   │   │   ├── assignment.py
│   │   │   └── submission.py
│   │   │
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── assignments.py
│   │   │   └── submissions.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── assignment.py
│   │   │   └── submission.py
│   │   │
│   │   ├── services/
│   │   │   ├── storage.py
│   │   │   └── supabase.py
│   │   │
│   │   ├── dependencies.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   │
│   ├── src/
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── cloud/
│   ├── supabase_schema.sql
│   ├── SUPABASE_SETUP.md
│   ├── render.yaml
│   └── Dockerfile.backend
│
├── tests/
│   ├── conftest.py
│   └── test_api.py
│
├── sample_files/
│
├── screenshots/
│
├── reports/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── CONCEPTS.md
│   ├── DEVELOPMENT_PLAN.md
│   ├── FAILURE_HANDLING.md
│   ├── IMPLEMENTATION_OPTIONS.md
│   ├── INTERVIEW.md
│   ├── PROOF_CHECKLIST.md
│   ├── REPORT.md
│   ├── SCALABILITY.md
│   ├── SECURITY.md
│   └── TEST_PLAN.md
│
├── README.md
├── Makefile
└── .gitignore
```

---

# Database Design

The application uses a relational database design.

## Main Tables

### USERS

Stores authentication and user information.

```text
USERS
-----
id
name
email
password_hash
role
created_at
```

Possible roles:

```text
student
teacher
```

### COURSES

Stores teacher-created courses.

```text
COURSES
-------
id
course_name
teacher_id
created_at
```

Relationship:

```text
Teacher
   |
   +---- Courses
```

### ASSIGNMENTS

Stores assignment information.

```text
ASSIGNMENTS
-----------
id
course_id
title
description
deadline
max_marks
allowed_file_types
max_file_size_mb
created_at
updated_at
```

Relationship:

```text
Course
   |
   +---- Assignments
```

### SUBMISSIONS

Stores submission metadata.

```text
SUBMISSIONS
-----------
id
assignment_id
student_id
file_name
file_path
file_size
submitted_at
status
marks
feedback
graded_at
```

Relationship:

```text
Assignment
    |
    +---- Submissions
                |
                +---- Student
```

---

# Database Relationships

```text
USERS
  |
  | teacher_id
  v
COURSES
  |
  | course_id
  v
ASSIGNMENTS
  |
  | assignment_id
  v
SUBMISSIONS
  ^
  |
  | student_id
  |
USERS
```

This structure keeps assignment metadata in the database while storing uploaded binary files separately.

---

# Assignment and Submission Workflow

## Step 1: Teacher Creates Course

```text
Teacher Login
      |
      v
Assignments
      |
      v
New Assignment
      |
      v
New Course
      |
      v
Create Course
```

## Step 2: Teacher Creates Assignment

```text
Select Course
      |
      v
Enter Assignment Details
      |
      v
Set Deadline
      |
      v
Set Maximum Marks
      |
      v
Set File Restrictions
      |
      v
Create Assignment
```

## Step 3: Student Views Assignment

```text
Student Login
      |
      v
Assignments
      |
      v
View Assignment
```

## Step 4: Student Uploads File

```text
Select Assignment
      |
      v
Choose File
      |
      v
Validate Extension
      |
      v
Validate File Size
      |
      v
Check Deadline
      |
      v
Store File
      |
      v
Create Submission Record
```

## Step 5: Teacher Reviews

```text
Teacher
   |
   v
Assignments
   |
   v
View Submissions
   |
   +---- Download File
   |
   +---- Enter Marks
   |
   +---- Add Feedback
   |
   v
Grade Submission
```

---

# File Storage

The application separates database metadata from uploaded binary files.

Example storage structure:

```text
storage/
│
└── assignments/
    │
    ├── assignment_1/
    │   ├── student_2/
    │   │   └── assignment.pdf
    │   │
    │   └── student_5/
    │       └── submission.docx
    │
    └── assignment_2/
        └── student_3/
            └── project.zip
```

This approach prevents large binary files from unnecessarily increasing database size.

The system can use either:

```text
Local Storage
```

or:

```text
Supabase Storage
```

depending on configuration.

---

# Authentication and Authorization

The application uses authentication and authorization as separate security layers.

## Authentication

Authentication answers:

```text
Who is the user?
```

The system validates credentials and issues an access token.

## Authorization

Authorization answers:

```text
What is the user allowed to do?
```

Example:

```text
Student
    |
    +-- View Assignments
    +-- Submit Work
    +-- View Own Submission
    +-- View Own Feedback

Teacher
    |
    +-- Create Courses
    +-- Create Assignments
    +-- Update Assignments
    +-- Delete Assignments
    +-- View Submissions
    +-- Grade Submissions
```

A student cannot access teacher-only endpoints.

A teacher cannot access another teacher's private resources without authorization.

---

# Frontend

The frontend is built using React and Vite.

The interface contains:

```text
Dashboard
Assignments
Teachers
Login
Register
```

The UI provides:

* Responsive layout
* Sidebar navigation
* Dashboard cards
* Assignment cards
* Search
* Forms
* Modal dialogs
* Loading states
* Error states
* Empty states
* Role-specific controls
* Course creation
* Assignment creation
* Assignment editing
* Assignment deletion

---

# Backend API

The FastAPI backend exposes RESTful endpoints.

## Health Check

```http
GET /api/health
```

Response:

```json
{
  "status": "ok",
  "service": "assignment-portal"
}
```

---

## Authentication

### Register

```http
POST /api/register
```

### Login

```http
POST /api/login
```

---

## Courses

### Get Courses

```http
GET /api/courses
```

### Create Course

```http
POST /api/courses
```

Example request:

```json
{
  "course_name": "Cloud Computing"
}
```

---

## Assignments

### Get Assignments

```http
GET /api/assignments
```

### Create Assignment

```http
POST /api/assignments
```

### Update Assignment

```http
PUT /api/assignments/{id}
```

### Delete Assignment

```http
DELETE /api/assignments/{id}
```

---

## Submissions

### Submit Assignment

```http
POST /api/assignments/{id}/submit
```

### Get My Submissions

```http
GET /api/submissions/me
```

### Grade Submission

```http
POST /api/submissions/{id}/grade
```

### Add Feedback

```http
POST /api/submissions/{id}/feedback
```

### Download Submission

```http
GET /api/submissions/{id}/download
```

---

# Local Development Setup

## Requirements

Install the following:

* Python 3.10+
* Node.js 18+
* npm
* Git

Recommended:

```text
Python 3.12
Node.js 20+
```

---

# Backend Setup

Open PowerShell or terminal.

Navigate to the project:

```powershell
cd "C:\Users\Akshay\Cloud Computing\Cloud-Based-Assignment-Submission-Portal"
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Install backend dependencies:

```powershell
python -m pip install -r backend\requirements.txt
```

---

# Backend Environment Configuration

Copy:

```text
backend/.env.example
```

to:

```text
backend/.env
```

Example:

```env
APP_NAME=Cloud Assignment Portal

SECRET_KEY=change-this-secret

ACCESS_TOKEN_EXPIRE_MINUTES=120

DATABASE_URL=sqlite:///./assignment_portal.db

STORAGE_BACKEND=local

AUTH_MODE=local

STORAGE_DIR=./storage

MAX_FILE_SIZE_MB=10

ALLOWED_EXTENSIONS=pdf,docx,txt,png,jpg,jpeg,zip

CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

For production, always replace development secrets with secure environment variables.

---

# Start Backend

Move into the backend directory:

```powershell
cd backend
```

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

Expected output:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

# Verify Backend

Open:

```text
http://127.0.0.1:8000/api/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "assignment-portal"
}
```

---

# Swagger API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# Frontend Setup

Open a second terminal.

Navigate to:

```powershell
cd "C:\Users\Akshay\Cloud Computing\Cloud-Based-Assignment-Submission-Portal\frontend"
```

Install dependencies:

```powershell
npm install
```

Start Vite:

```powershell
npm run dev
```

Expected output:

```text
VITE ready

Local:
http://localhost:5173/
```

Open:

```text
http://localhost:5173
```

---

# Running Backend and Frontend Together

You need two terminals.

## Terminal 1

```powershell
cd "C:\Users\Akshay\Cloud Computing\Cloud-Based-Assignment-Submission-Portal\backend"

uvicorn app.main:app --reload
```

## Terminal 2

```powershell
cd "C:\Users\Akshay\Cloud Computing\Cloud-Based-Assignment-Submission-Portal\frontend"

npm run dev
```

Application:

```text
http://localhost:5173
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Creating a Teacher Course

A teacher must have a course before creating an assignment.

The workflow is:

```text
Teacher Login
      |
      v
Assignments
      |
      v
New Assignment
      |
      v
New Course
      |
      v
Enter Course Name
      |
      v
Create Course
      |
      v
Course Automatically Appears
      |
      v
Select Course
      |
      v
Create Assignment
```

Example:

```text
Course Name:
Cloud Computing
```

Then the assignment form can use:

```text
Course:
Cloud Computing
```

This prevents the assignment from being created without a valid course relationship.

---

# Testing

The project includes automated API tests.

From the project root:

```powershell
cd backend
pytest ../tests -q
```

Testing covers important application functionality such as:

* Health endpoint
* Authentication
* Protected routes
* Assignment workflows
* Submission workflows
* Role-based authorization

---

# Security

The application implements several security practices.

## Password Security

Passwords are hashed instead of being stored as plain text.

```text
Plain Password
      |
      v
Password Hash
      |
      v
Database
```

## JWT Authentication

Authenticated users receive access tokens.

Protected endpoints require valid authentication.

## Role-Based Authorization

Teacher-only functionality is protected.

Student-only resources are also restricted.

## File Validation

Uploaded files are validated using:

* File extension
* Maximum file size
* Assignment-specific restrictions

## Private Submission Access

Students can access their own submissions while teacher access is controlled by assignment ownership and authorization.

## Environment Variables

Sensitive configuration should not be hard-coded.

Examples:

```text
SECRET_KEY
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
DATABASE_URL
```

These should be stored in environment variables.

---

# Scalability

The architecture is designed to support future scaling.

## Current Architecture

```text
React
  |
FastAPI
  |
Database
  |
Local Storage
```

## Cloud Architecture

```text
React Static Hosting
        |
     API Layer
        |
    FastAPI Service
        |
  +-----+------+
  |            |
PostgreSQL   Object Storage
  |            |
Supabase     Supabase Storage
```

Potential future improvements include:

* CDN
* API Gateway
* Managed PostgreSQL
* Object storage
* Serverless components
* Horizontal backend scaling
* Background processing
* Caching
* Centralized logging
* Monitoring

---

# Failure Handling

The application considers several common failure scenarios.

## Invalid Login

The user receives an authentication error.

## Invalid File

The upload is rejected when:

* File extension is not allowed
* File exceeds the maximum size

## Expired Deadline

Submission status can be marked as late according to the assignment deadline logic.

## Unauthorized Access

Protected resources return authorization errors when accessed by users without the required role or ownership.

## Missing Course

A teacher cannot create an assignment without selecting a valid course.

The interface provides a `New Course` option so the teacher can create a course directly from the assignment form.

## Database Failure

The application is designed so that database errors can be handled by the API layer without exposing sensitive implementation details to users.

---

# Cloud Deployment

The application can be migrated from local development to cloud services.

## Supabase

Possible services:

```text
Supabase PostgreSQL
Supabase Authentication
Supabase Storage
```

Architecture:

```text
React
  |
FastAPI
  |
  +------ Supabase PostgreSQL
  |
  +------ Supabase Storage
```

---

# AWS Mapping

A possible AWS deployment architecture:

```text
React
   |
CloudFront
   |
S3 Static Hosting
   |
API Gateway / Load Balancer
   |
FastAPI
   |
RDS PostgreSQL
   |
S3 Object Storage
```

---

# Microsoft Azure Mapping

Possible services:

```text
Azure Static Web Apps
Azure App Service
Azure Database for PostgreSQL
Azure Blob Storage
Azure Monitor
```

---

# Google Cloud Mapping

Possible services:

```text
Cloud Storage
Cloud Run
Cloud SQL
Cloud Load Balancing
Cloud Monitoring
```

---

# Environment Modes

The project supports a local development configuration and a cloud-ready configuration.

## Local

```env
AUTH_MODE=local
STORAGE_BACKEND=local
DATABASE_URL=sqlite:///./assignment_portal.db
```

## Cloud

Example:

```env
AUTH_MODE=supabase
STORAGE_BACKEND=supabase
DATABASE_URL=<POSTGRES_CONNECTION_STRING>
SUPABASE_URL=<SUPABASE_PROJECT_URL>
SUPABASE_SERVICE_ROLE_KEY=<SUPABASE_SERVICE_ROLE_KEY>
SUPABASE_STORAGE_BUCKET=assignments
```

Never commit real production credentials to GitHub.

---

# GitHub Setup

Initialize Git:

```powershell
git init
```

Check files:

```powershell
git status
```

Add files:

```powershell
git add .
```

Create commit:

```powershell
git commit -m "Initial cloud assignment portal implementation"
```

Add remote:

```powershell
git remote add origin YOUR_GITHUB_REPOSITORY_URL
```

Push:

```powershell
git branch -M main
git push -u origin main
```

---

# Important GitHub Security Rules

Never commit:

```text
.env
.venv/
__pycache__/
*.db
storage/
node_modules/
```

The project includes a `.gitignore` file for this purpose.

Before pushing:

```powershell
git status
```

Make sure secrets are not included.

---

# Suggested GitHub Repository Topics

You can add topics such as:

```text
cloud-computing
react
fastapi
python
javascript
vite
postgresql
sqlite
supabase
rest-api
jwt
role-based-access-control
file-upload
assignment-management
student-portal
education-technology
full-stack
```

---

# Project Documentation

Additional technical documentation is available inside the `docs/` directory.

## Architecture

```text
docs/ARCHITECTURE.md
```

Contains the system architecture and component relationships.

## Cloud Concepts

```text
docs/CONCEPTS.md
```

Explains the cloud computing concepts demonstrated by the project.

## API Documentation

```text
docs/API.md
```

Contains API endpoint information.

## Security

```text
docs/SECURITY.md
```

Documents authentication, authorization, file validation and security practices.

## Scalability

```text
docs/SCALABILITY.md
```

Explains how the system can be scaled.

## Failure Handling

```text
docs/FAILURE_HANDLING.md
```

Documents application failure scenarios and handling strategies.

## Testing

```text
docs/TEST_PLAN.md
```

Contains the project testing approach.

## Development Plan

```text
docs/DEVELOPMENT_PLAN.md
```

Contains the implementation and development plan.

## Interview Preparation

```text
docs/INTERVIEW.md
```

Contains technical interview questions and project explanations.

## Project Report

```text
docs/REPORT.md
```

Contains the project report structure and technical explanation.

---

# Recommended Demo Flow

For a project demonstration, use the following sequence.

## 1. Register Teacher

```text
Register
    |
Role: Teacher
```

## 2. Login as Teacher

```text
Teacher Dashboard
```

## 3. Create Course

```text
Assignments
    |
New Assignment
    |
New Course
    |
Cloud Computing
```

## 4. Create Assignment

```text
Course:
Cloud Computing

Title:
Cloud Architecture Assignment

Maximum Marks:
100

Deadline:
Future Date
```

## 5. Register Student

```text
Register
    |
Role: Student
```

## 6. Login as Student

View the assignment.

## 7. Submit File

Upload:

```text
assignment.pdf
```

## 8. Login as Teacher

Open submissions.

## 9. Grade

Example:

```text
Marks:
88

Feedback:
Good implementation and clear explanation.
```

## 10. Login as Student Again

View:

```text
Status: GRADED
Marks: 88
Feedback: Good implementation and clear explanation.
```

This demonstrates the complete end-to-end workflow.

---

# Cloud Computing Concepts Demonstrated

This project demonstrates practical cloud computing concepts including:

### Infrastructure and Application Hosting

The application is designed for deployment using cloud-hosted frontend and backend services.

### Managed Database

PostgreSQL/Supabase can be used as the managed database layer.

### Object Storage

Assignment submissions are designed to use object storage instead of storing binary files directly in database rows.

### Authentication

User authentication provides secure access to the application.

### Authorization

RBAC ensures that users can only access permitted functionality.

### REST APIs

The frontend communicates with the backend using REST APIs.

### Scalability

The architecture separates:

```text
Frontend
Backend
Database
Storage
```

allowing individual components to scale independently.

### Security

The system demonstrates:

```text
Password Hashing
JWT
RBAC
Input Validation
File Validation
Environment Variables
Protected Routes
```

---

# Learning Outcomes

Through this project, the following practical skills are demonstrated:

* Full-stack application development
* React development
* FastAPI development
* REST API design
* JWT authentication
* Role-based authorization
* SQL database design
* SQLAlchemy ORM
* File upload systems
* Object storage architecture
* Cloud-ready application design
* Supabase integration
* PostgreSQL
* API testing
* Git and GitHub
* Environment configuration
* Application security
* Deployment architecture
* Scalability planning
* Failure handling

---

# Project Status

Current implementation includes:

```text
Authentication                 Implemented
Role-Based Access Control     Implemented
Student Dashboard             Implemented
Teacher Dashboard             Implemented
Course Management             Implemented
Assignment CRUD               Implemented
Assignment Search             Implemented
File Upload                   Implemented
File Resubmission             Implemented
Deadline Handling             Implemented
Submission Tracking            Implemented
Grading                       Implemented
Teacher Feedback              Implemented
Local Database                Implemented
Local File Storage            Implemented
Cloud Storage Adapter         Implemented
Supabase Integration          Supported
REST API                      Implemented
Swagger Documentation         Implemented
Automated API Tests           Included
Cloud Deployment Structure    Included
```

---




---


# License

This project is developed for educational, academic, portfolio, and demonstration purposes.

If you reuse or extend this project, please provide appropriate attribution.

---

# Final Architecture Summary

```text
                         CLOUD ASSIGNMENT PORTAL
                                  |
              +-------------------+-------------------+
              |                                       |
           STUDENT                                TEACHER
              |                                       |
           Login                                    Login
              |                                       |
         Dashboard                              Dashboard
              |                                       |
        Assignments                            Courses
              |                                       |
       Submit Work                         Create Assignment
              |                                       |
        Submission                         View Submissions
              |                                       |
          Status                               Grade Work
              |                                       |
           Marks                                Feedback
              |                                       |
              +-------------------+-------------------+
                                  |
                              REST API
                                  |
                               FastAPI
                                  |
                +-----------------+-----------------+
                |                                   |
             Database                         File Storage
                |                                   |
        SQLite / PostgreSQL               Local / Supabase
                |
          Users / Courses
        Assignments / Submissions
```

---

## Conclusion

The Cloud-Based Student Assignment Submission & Feedback Portal demonstrates how a practical academic management system can be designed using modern full-stack development and cloud computing principles.

The project combines frontend development, backend REST APIs, authentication, role-based authorization, relational database design, file storage, cloud integration, testing, security, scalability, and deployment architecture into a single end-to-end application.
