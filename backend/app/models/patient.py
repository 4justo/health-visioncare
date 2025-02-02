from sqlalchemy import Column, String, Integer, Enum, Date, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from .base import BaseModel
from ..core.database import Base
import enum

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class BloodType(str, enum.Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"

class Patient(BaseModel, Base):
    __tablename__ = "patients"
    
    # Personal Information
    patient_id = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    
    # Contact Information
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    
    # Medical Information
    blood_type = Column(Enum(BloodType), nullable=True)
    allergies = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)
    current_medications = Column(Text, nullable=True)
    
    # Clinic Information
    clinic_name = Column(String(255), nullable=True)
    clinic_address = Column(Text, nullable=True)
    primary_physician = Column(String(255), nullable=True)
    referral_source = Column(String(255), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_deceased = Column(Boolean, default=False)
    
    # Metadata
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    last_visit_date = Column(DateTime(timezone=True), nullable=True)
    next_appointment = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    notes = Column(Text, nullable=True)
    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relation = Column(String(100), nullable=True)
