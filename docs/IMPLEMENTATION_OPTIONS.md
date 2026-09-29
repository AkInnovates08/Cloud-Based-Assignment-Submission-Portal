# Three Implementation Options

## Option A — Beginner
Frontend: HTML/CSS/JavaScript
Backend: Flask
Database: SQLite
Storage: local uploads

Difficulty: Low
Cost: $0 locally
Purpose: learn CRUD, HTTP and file handling
Limitation: weak cloud proof

## Option B — Recommended
Frontend: React
Backend: FastAPI
Authentication: Supabase Auth or equivalent
Database: Supabase PostgreSQL
Storage: Supabase Storage
Deployment: free/static frontend + free backend where available

Difficulty: Medium
Cost: suitable for student/hobby use within current provider limits
Cloud proof: strong
Limitation: provider-specific configuration

## Option C — Advanced
Frontend: React/Next.js
Backend: FastAPI/serverless
Cloud: AWS/Azure/GCP
API Gateway + managed DB + object storage + managed auth + monitoring

Difficulty: High
Cost: depends on provider usage
Cloud proof: strongest infrastructure exposure
Limitation: more setup and possible billing risk

## Recommendation
Build Option B after completing the local simulation. Keep Option A as the reproducible offline baseline and use Option C as an architecture discussion/deployment extension.
