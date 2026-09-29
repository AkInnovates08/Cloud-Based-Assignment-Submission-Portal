# Cloud Computing Concepts Mapped to the Project

| Concept | Where it appears |
|---|---|
| Cloud Computing | Hosted React/API/database/storage services |
| SaaS | The portal is consumed through a browser |
| PaaS | Managed app hosting such as Render |
| IaaS | AWS EC2/Azure VM/GCE alternative |
| Cloud Database | Supabase PostgreSQL or managed PostgreSQL |
| Object Storage | Supabase Storage / S3 / Azure Blob / GCS |
| Authentication | Local JWT in demo; Supabase Auth in cloud architecture |
| Authorization | Role checks in FastAPI |
| RBAC | `student` and `teacher` permissions |
| REST API | `/api/...` endpoints |
| Serverless | Optional Lambda/Functions mapping |
| Scalability | Stateless API + managed DB + object storage |
| Elasticity | Autoscaling/serverless in advanced deployment |
| Availability | Managed services, health checks, multiple service layers |
| Load Balancing | Cloud load balancer in scaled deployment |
| CDN | Static frontend/CDN in production architecture |
| API Gateway | AWS API Gateway or equivalent in advanced version |
| Environment Variables | `.env` and cloud secret configuration |
| Secrets Management | Hosting provider secrets / cloud secret manager |
| Logging | Python logging and provider logs |
| Monitoring | Health endpoint + cloud observability |
| Backup | Managed DB backups on plans that provide them |
| CI/CD | Git push → cloud build/deploy |
