from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ...core.database import get_db
from ...core.auth import get_current_user, require_role
from ...services.patient_service import PatientService
from ...schemas.patient import (
    PatientCreate, PatientUpdate, PatientResponse,
    PatientListResponse, PatientSearchParams
)
from ...models.user import User

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_data: PatientCreate,
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Create a new patient"""
    patient = PatientService.create_patient(db, patient_data, current_user.id)
    return patient

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: str,
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Get patient by ID"""
    patient = PatientService.get_patient(db, patient_id)
    return patient

@router.get("/by-patient-id/{patient_id}", response_model=PatientResponse)
async def get_patient_by_patient_id(
    patient_id: str,
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Get patient by patient_id"""
    patient = PatientService.get_patient_by_patient_id(db, patient_id)
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: str,
    patient_data: PatientUpdate,
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Update a patient"""
    patient = PatientService.update_patient(db, patient_id, patient_data, current_user.id)
    return patient

@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: str,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Delete a patient (admin only)"""
    PatientService.delete_patient(db, patient_id)
    return {"message": "Patient deleted successfully"}

@router.delete("/{patient_id}/hard")
async def hard_delete_patient(
    patient_id: str,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Hard delete a patient (admin only)"""
    PatientService.hard_delete_patient(db, patient_id)
    return {"message": "Patient permanently deleted"}

@router.get("/", response_model=PatientListResponse)
async def search_patients(
    search: Optional[str] = Query(None, description="Search term"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    clinic_name: Optional[str] = Query(None, description="Filter by clinic"),
    created_after: Optional[datetime] = Query(None, description="Filter by creation date"),
    created_before: Optional[datetime] = Query(None, description="Filter by creation date"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("created_at", description="Sort by field"),
    sort_order: str = Query("desc", description="Sort order"),
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Search patients with filters and pagination"""
    params = PatientSearchParams(
        search=search,
        gender=gender,
        is_active=is_active,
        clinic_name=clinic_name,
        created_after=created_after,
        created_before=created_before,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    result = PatientService.search_patients(db, params)
    return result

@router.get("/stats")
async def get_patient_stats(
    current_user: User = Depends(require_role(["admin", "doctor"])),
    db: Session = Depends(get_db)
):
    """Get patient statistics"""
    stats = PatientService.get_patient_stats(db)
    return stats

@router.get("/recent/", response_model=List[PatientResponse])
async def get_recent_patients(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Get recently created patients"""
    patients = PatientService.get_recent_patients(db, limit)
    return patients

@router.get("/{patient_id}/history")
async def get_patient_history(
    patient_id: str,
    current_user: User = Depends(require_role(["admin", "doctor", "technician"])),
    db: Session = Depends(get_db)
):
    """Get patient history including scans"""
    history = PatientService.get_patient_history(db, patient_id)
    return history
