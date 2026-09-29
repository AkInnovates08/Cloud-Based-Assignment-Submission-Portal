from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.routes import auth, assignments, submissions, dashboard, health

app = FastAPI(
    title="Cloud-Based Assignment Submission & Feedback Portal",
    version="1.0.0",
    description="Industry-oriented Cloud Computing course project."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(assignments.router, prefix="/api")
app.include_router(submissions.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
