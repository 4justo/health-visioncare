from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum, Float, Boolean, JSON, Integer
from sqlalchemy.sql import func
from .base import BaseModel
from ..core.database import Base
import enum

class ScanStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ScanType(str, enum.Enum):
    RETINAL = "retinal"
    OCT = "oct"
    FUNDUS = "fundus"

class Scan(BaseModel, Base):
    __tablename__ = "scans"
    
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    scan_type = Column(Enum(ScanType), nullable=False)
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    status = Column(Enum(ScanStatus), default=ScanStatus.PENDING)
    
    # Image metadata
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)
    image_width = Column(Integer, nullable=True)
    image_height = Column(Integer, nullable=True)
    image_quality = Column(Float, nullable=True)
    
    # AI Results
    ai_prediction = Column(String(100), nullable=True)
    ai_confidence = Column(Float, nullable=True)
    ai_processing_time = Column(Float, nullable=True)
    ai_model_version = Column(String(50), nullable=True)
    ai_results = Column(JSON, nullable=True)
    
    # Metadata
    captured_date = Column(DateTime(timezone=True), nullable=False)
    uploaded_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    processed_date = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Grad-CAM
    heatmap_url = Column(String(500), nullable=True)
    overlay_url = Column(String(500), nullable=True)
    
    # Security
    is_secure = Column(Boolean, default=True)
