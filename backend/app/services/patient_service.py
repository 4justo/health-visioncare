from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func, desc, asc
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import uuid

from ..models.patient import Patient, Gender
from ..models.user import User
from ..schemas.patient import PatientCreate, PatientUpdate, PatientSearchParams
from ..core.config import settings

class PatientService:
    @staticmethod
    def generate_patient_id(db: Session) -> str:
        """Generate a unique patient ID"""
        year = datetime.now().year
        count = db.query(Patient).filter(
            Patient.patient_id.like(f"PAT-{year}-%")
        ).count()
        return f"PAT-{year}-{count + 1:04d}"
    
    @staticmethod
    def create_patient(db: Session, patient_data: PatientCreate, user_id: str) -> Patient:
        """Create a new patient"""
        # Check for duplicate email or phone
        if patient_data.email:
            existing = db.query(Patient).filter(
                Patient.email == patient_data.email
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Patient with this email already exists"
                )
        
        if patient_data.phone:
            existing = db.query(Patient).filter(
                Patient.phone == patient_data.phone
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Patient with this phone number already exists"
                )
        
        # Create new patient
        new_patient = Patient(
            patient_id=PatientService.generate_patient_id(db),
            first_name=patient_data.first_name,
            last_name=patient_data.last_name,
            date_of_birth=patient_data.date_of_birth,
            gender=patient_data.gender,
            email=patient_data.email,
            phone=patient_data.phone,
            address=patient_data.address,
            city=patient_data.city,
            state=patient_data.state,
            zip_code=patient_data.zip_code,
            country=patient_data.country,
            blood_type=patient_data.blood_type,
            allergies=patient_data.allergies,
            medical_history=patient_data.medical_history,
            current_medications=patient_data.current_medications,
            clinic_name=patient_data.clinic_name,
            clinic_address=patient_data.clinic_address,
            primary_physician=patient_data.primary_physician,
            referral_source=patient_data.referral_source,
            emergency_contact_name=patient_data.emergency_contact_name,
            emergency_contact_phone=patient_data.emergency_contact_phone,
            emergency_contact_relation=patient_data.emergency_contact_relation,
            notes=patient_data.notes,
            created_by=user_id
        )
        
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        
        return new_patient
    
    @staticmethod
    def get_patient(db: Session, patient_id: str) -> Patient:
        """Get a patient by ID"""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        return patient
    
    @staticmethod
    def get_patient_by_patient_id(db: Session, patient_id: str) -> Patient:
        """Get a patient by patient_id"""
        patient = db.query(Patient).filter(
            Patient.patient_id == patient_id
        ).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        return patient
    
    @staticmethod
    def update_patient(
        db: Session,
        patient_id: str,
        patient_data: PatientUpdate,
        user_id: str
    ) -> Patient:
        """Update a patient"""
        patient = PatientService.get_patient(db, patient_id)
        
        # Check for duplicate email/phone if updating
        if patient_data.email and patient_data.email != patient.email:
            existing = db.query(Patient).filter(
                Patient.email == patient_data.email
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Patient with this email already exists"
                )
        
        if patient_data.phone and patient_data.phone != patient.phone:
            existing = db.query(Patient).filter(
                Patient.phone == patient_data.phone
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Patient with this phone number already exists"
                )
        
        # Update fields
        update_data = patient_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(patient, field, value)
        
        patient.updated_by = user_id
        patient.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(patient)
        
        return patient
    
    @staticmethod
    def delete_patient(db: Session, patient_id: str) -> bool:
        """Soft delete a patient (admin only)"""
        patient = PatientService.get_patient(db, patient_id)
        patient.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def hard_delete_patient(db: Session, patient_id: str) -> bool:
        """Hard delete a patient (admin only)"""
        patient = PatientService.get_patient(db, patient_id)
        db.delete(patient)
        db.commit()
        return True
    
    @staticmethod
    def search_patients(
        db: Session,
        params: PatientSearchParams,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search patients with filters and pagination"""
        query = db.query(Patient).filter(Patient.is_active == True)
        
        # Search by name, patient_id, email, phone
        if params.search:
            search_term = f"%{params.search}%"
            query = query.filter(
                or_(
                    Patient.first_name.ilike(search_term),
                    Patient.last_name.ilike(search_term),
                    Patient.patient_id.ilike(search_term),
                    Patient.email.ilike(search_term),
                    Patient.phone.ilike(search_term)
                )
            )
        
        # Filter by gender
        if params.gender:
            query = query.filter(Patient.gender == params.gender)
        
        # Filter by clinic
        if params.clinic_name:
            query = query.filter(
                Patient.clinic_name.ilike(f"%{params.clinic_name}%")
            )
        
        # Filter by date range
        if params.created_after:
            query = query.filter(Patient.created_at >= params.created_after)
        if params.created_before:
            query = query.filter(Patient.created_at <= params.created_before)
        
        # Get total count
        total = query.count()
        
        # Sorting
        sort_column = getattr(Patient, params.sort_by, Patient.created_at)
        if params.sort_order == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Pagination
        offset = (params.page - 1) * params.size
        query = query.offset(offset).limit(params.size)
        
        # Execute query
        patients = query.all()
        
        # Calculate age for each patient
        today = date.today()
        for patient in patients:
            age = today.year - patient.date_of_birth.year
            if today.month < patient.date_of_birth.month or \
               (today.month == patient.date_of_birth.month and today.day < patient.date_of_birth.day):
                age -= 1
            patient.age = age
        
        return {
            "items": patients,
            "total": total,
            "page": params.page,
            "size": params.size,
            "pages": (total + params.size - 1) // params.size
        }
    
    @staticmethod
    def get_patient_stats(db: Session) -> Dict[str, Any]:
        """Get patient statistics"""
        total = db.query(Patient).filter(Patient.is_active == True).count()
        
        # Gender distribution
        male_count = db.query(Patient).filter(
            Patient.is_active == True,
            Patient.gender == Gender.MALE
        ).count()
        female_count = db.query(Patient).filter(
            Patient.is_active == True,
            Patient.gender == Gender.FEMALE
        ).count()
        other_count = db.query(Patient).filter(
            Patient.is_active == True,
            Patient.gender == Gender.OTHER
        ).count()
        
        # Age distribution
        today = date.today()
        age_groups = {
            "0-18": 0,
            "19-35": 0,
            "36-50": 0,
            "51-65": 0,
            "65+": 0
        }
        
        patients = db.query(Patient).filter(Patient.is_active == True).all()
        for patient in patients:
            age = today.year - patient.date_of_birth.year
            if today.month < patient.date_of_birth.month or \
               (today.month == patient.date_of_birth.month and today.day < patient.date_of_birth.day):
                age -= 1
            
            if age <= 18:
                age_groups["0-18"] += 1
            elif age <= 35:
                age_groups["19-35"] += 1
            elif age <= 50:
                age_groups["36-50"] += 1
            elif age <= 65:
                age_groups["51-65"] += 1
            else:
                age_groups["65+"] += 1
        
        # Recent patients (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent = db.query(Patient).filter(
            Patient.is_active == True,
            Patient.created_at >= week_ago
        ).count()
        
        return {
            "total": total,
            "gender_distribution": {
                "male": male_count,
                "female": female_count,
                "other": other_count
            },
            "age_groups": age_groups,
            "recent_patients": recent,
            "clinic_count": db.query(Patient.clinic_name).filter(
                Patient.is_active == True,
                Patient.clinic_name.isnot(None)
            ).distinct().count()
        }
    
    @staticmethod
    def get_recent_patients(db: Session, limit: int = 10) -> List[Patient]:
        """Get recently created patients"""
        return db.query(Patient).filter(
            Patient.is_active == True
        ).order_by(
            desc(Patient.created_at)
        ).limit(limit).all()
    
    @staticmethod
    def get_patient_history(db: Session, patient_id: str) -> Dict[str, Any]:
        """Get patient history including scans and visits"""
        patient = PatientService.get_patient(db, patient_id)
        
        # Get scans
        scans = db.query(Scan).filter(
            Scan.patient_id == patient_id
        ).order_by(
            desc(Scan.captured_date)
        ).all()
        
        # Get visit history (future module)
        visits = []  # Will be implemented in Module 8
        
        return {
            "patient": patient,
            "scans": scans,
            "visits": visits,
            "total_scans": len(scans)
        }
