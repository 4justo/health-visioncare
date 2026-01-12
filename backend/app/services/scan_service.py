from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException, status, UploadFile
from typing import Optional, Dict, Any
from datetime import datetime
import os
import io

from ..models.scan import Scan, ScanStatus, ScanType
from ..models.patient import Patient
from ..schemas.scan import ScanUpdate
from .image_service import ImageService
from .storage_service import StorageService
from ..core.config import settings

class ScanService:
    storage_service = StorageService()
    
    @staticmethod
    async def upload_scan(
        db: Session,
        patient_id: str,
        file: UploadFile,
        scan_type: ScanType,
        user_id: str,
        notes: str = None,
        captured_date: datetime = None
    ) -> Dict[str, Any]:
        """Upload and process a scan"""
        # Validate patient exists
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        # Validate image
        is_valid, error_message = ImageService.validate_image(file)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Create scan record
        if not captured_date:
            captured_date = datetime.utcnow()
        
        # Read file content for size
        content = await file.read()
        file_size = len(content)
        
        # Reset file position for saving
        file.file = io.BytesIO(content)
        
        scan = Scan(
            patient_id=patient_id,
            scan_type=scan_type,
            status=ScanStatus.PROCESSING,
            file_name=file.filename,
            file_size=file_size,
            file_type=file.content_type,
            uploaded_by=user_id,
            captured_date=captured_date,
            notes=notes
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        try:
            # Save uploaded file
            upload_dir = os.path.join(settings.UPLOAD_DIR, 'temp')
            saved_file = await ImageService.save_upload(file, upload_dir)
            
            # Get image metadata
            if saved_file['metadata']:
                scan.image_width = saved_file['metadata']['width']
                scan.image_height = saved_file['metadata']['height']
            
            # Create thumbnail
            thumb_dir = os.path.join(settings.UPLOAD_DIR, 'thumbnails')
            thumb_path = await ImageService.create_thumbnail(
                saved_file['file_path'],
                thumb_dir
            )
            
            # Upload to storage
            scan_key = f"scans/{scan.id}_{saved_file['filename']}"
            image_url = await ScanService.storage_service.upload_file(
                saved_file['file_path'],
                scan_key,
                file.content_type
            )
            
            # Upload thumbnail
            if thumb_path:
                thumb_key = f"thumbnails/{scan.id}_thumb_{saved_file['filename']}"
                thumb_url = await ScanService.storage_service.upload_file(
                    thumb_path,
                    thumb_key,
                    'image/jpeg'
                )
                scan.thumbnail_url = thumb_url
            
            # Update scan record
            scan.image_url = image_url
            scan.status = ScanStatus.PENDING
            
            # Cleanup temp files
            await ImageService.cleanup_temp_file(saved_file['file_path'])
            if thumb_path:
                await ImageService.cleanup_temp_file(thumb_path)
            
            db.commit()
            db.refresh(scan)
            
            return {
                'scan': scan,
                'message': 'Scan uploaded successfully'
            }
            
        except Exception as e:
            scan.status = ScanStatus.FAILED
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process scan: {str(e)}"
            )
    
    @staticmethod
    def get_scan(db: Session, scan_id: str) -> Scan:
        """Get a scan by ID"""
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan not found"
            )
        return scan
    
    @staticmethod
    def get_patient_scans(
        db: Session,
        patient_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get all scans for a patient"""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        query = db.query(Scan).filter(Scan.patient_id == patient_id)
        total = query.count()
        scans = query.order_by(desc(Scan.captured_date)).offset(skip).limit(limit).all()
        
        return {
            'items': scans,
            'total': total,
            'page': (skip // limit) + 1 if limit > 0 else 1,
            'size': limit,
            'pages': (total + limit - 1) // limit if limit > 0 else 1
        }
    
    @staticmethod
    def update_scan(
        db: Session,
        scan_id: str,
        scan_data: ScanUpdate,
        user_id: str
    ) -> Scan:
        """Update a scan"""
        scan = ScanService.get_scan(db, scan_id)
        
        update_data = scan_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(scan, field, value)
        
        db.commit()
        db.refresh(scan)
        
        return scan
    
    @staticmethod
    def delete_scan(db: Session, scan_id: str) -> bool:
        """Delete a scan"""
        scan = ScanService.get_scan(db, scan_id)
        
        db.delete(scan)
        db.commit()
        return True
