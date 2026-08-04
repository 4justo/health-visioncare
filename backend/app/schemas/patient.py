from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class BloodType(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"

class PatientCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: Gender
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    
    blood_type: Optional[BloodType] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    primary_physician: Optional[str] = None
    referral_source: Optional[str] = None
    
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    
    notes: Optional[str] = None

class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    
    blood_type: Optional[BloodType] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    primary_physician: Optional[str] = None
    referral_source: Optional[str] = None
    
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    
    is_active: Optional[bool] = None
    is_deceased: Optional[bool] = None
    notes: Optional[str] = None

class PatientResponse(BaseModel):
    id: str
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    age: Optional[int] = None
    
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    
    blood_type: Optional[BloodType] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    primary_physician: Optional[str] = None
    referral_source: Optional[str] = None
    
    is_active: bool
    is_deceased: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_visit_date: Optional[datetime]
    next_appointment: Optional[datetime]
    created_by: str
    notes: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    
    class Config:
        from_attributes = True

class PatientListResponse(BaseModel):
    items: List[PatientResponse]
    total: int
    page: int
    size: int
    pages: int

class PatientSearchParams(BaseModel):
    search: Optional[str] = None
    gender: Optional[Gender] = None
    is_active: Optional[bool] = None
    clinic_name: Optional[str] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    page: int = 1
    size: int = 10
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
