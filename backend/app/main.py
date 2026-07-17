from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
from pathlib import Path

from app.config import settings
from app.database import init_db, engine, Base
from app.routes import auth, student, faculty, attendance, result, fee, placement, timetable, notice, complaint, ai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CampusAI",
    description="Comprehensive Campus Management System with AI Integration",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables"""
    init_db()
    logger.info("Database initialized")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": "production" if not settings.DEBUG else "development"
    }

# Include routers
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(faculty.router)
app.include_router(attendance.router)
app.include_router(result.router)
app.include_router(fee.router)
app.include_router(placement.router)
app.include_router(timetable.router)
app.include_router(notice.router)
app.include_router(complaint.router)
app.include_router(ai.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CampusAI API",
        "docs": "/api/docs",
        "openapi": "/api/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
