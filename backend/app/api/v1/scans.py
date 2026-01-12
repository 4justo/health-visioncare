from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ...core.database import get_db
from ...core.auth import require_role
from ...services.scan_service import ScanService
from ...schemas.scan import (
    ScanResponse, ScanUploadResponse, ScanUpdate, ScanListResponse, ScanType
)
from ...models.user import User

router = APIRouter(prefix="/scans", tags=["scans"])

@router.post("/upload", response_model=ScanUploadResponse)
async def upload_scan(
    patient_id: str = Form(...),
    scan_type: ScanType = Form(...),
    file: UploadFile = File(...),
    notes: Optional[str] = Form(None),
    captured_date: Optional[datetime] = Form(None),
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Upload a new scan for a patient"""
    result = await ScanService.upload_scan(
        db=db,
        patient_id=patient_id,
        file=file,
        scan_type=scan_type,
        user_id=current_user.id,
        notes=notes,
        captured_date=captured_date
    )
    
    return ScanUploadResponse(
        scan=result['scan'],
        message=result['message']
    )

@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(
    scan_id: str,
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Get a scan by ID"""
    scan = ScanService.get_scan(db, scan_id)
    return scan

@router.get("/patient/{patient_id}", response_model=ScanListResponse)
async def get_patient_scans(
    patient_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Get all scans for a patient"""
    skip = (page - 1) * size
    result = ScanService.get_patient_scans(db, patient_id, skip, size)
    return result

@router.put("/{scan_id}", response_model=ScanResponse)
async def update_scan(
    scan_id: str,
    scan_data: ScanUpdate,
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Update a scan"""
    scan = ScanService.update_scan(db, scan_id, scan_data, current_user.id)
    return scan

@router.delete("/{scan_id}")
async def delete_scan(
    scan_id: str,
    current_user: User = Depends(require_role(["admin", "doctor"])),
    db: Session = Depends(get_db)
):
    """Delete a scan"""
    ScanService.delete_scan(db, scan_id)
    return {"message": "Scan deleted successfully"}
