from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "VisionCare API",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/health/db")
async def db_health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }