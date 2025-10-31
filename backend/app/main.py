from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import auth, gmail, analysis, sheets, calendar, reminders

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Kesu AI Email Intelligence API")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down Kesu AI Email Intelligence API")

app = FastAPI(
    title="Kesu AI Email Intelligence API",
    description="AI-powered Gmail management system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(gmail.router, prefix=f"{settings.API_V1_PREFIX}/gmail", tags=["Gmail"])
app.include_router(analysis.router, prefix=f"{settings.API_V1_PREFIX}/analysis", tags=["Analysis"])
app.include_router(sheets.router, prefix=f"{settings.API_V1_PREFIX}/sheets", tags=["Google Sheets"])
app.include_router(calendar.router, prefix=f"{settings.API_V1_PREFIX}/calendar", tags=["Calendar"])
app.include_router(reminders.router, prefix=f"{settings.API_V1_PREFIX}/reminders", tags=["Reminders"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Kesu AI Email Intelligence API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
