from PIL import Image
import os
import uuid
from datetime import datetime
from typing import Tuple, Optional
import io
import shutil
from pathlib import Path
import asyncio
import aiofiles
import hashlib

class ImageService:
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
    ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/tiff', 'image/bmp'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    THUMBNAIL_SIZE = (300, 300)
    PROCESSED_SIZE = (1024, 1024)
    
    @staticmethod
    def validate_image(file) -> Tuple[bool, str]:
        """Validate image file"""
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ImageService.ALLOWED_EXTENSIONS:
            return False, f"File type {file_ext} not allowed. Allowed: {', '.join(ImageService.ALLOWED_EXTENSIONS)}"
        
        # Check MIME type
        if file.content_type not in ImageService.ALLOWED_MIME_TYPES:
            return False, f"Invalid MIME type: {file.content_type}"
        
        return True, "Valid"
    
    @staticmethod
    async def save_upload(file, upload_dir: str) -> dict:
        """Save uploaded file to disk"""
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_id = uuid.uuid4().hex
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}{file_ext}"
        
        # Create full path
        file_path = os.path.join(upload_dir, filename)
        
        # Ensure directory exists
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file asynchronously
        content = await file.read()
        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(content)
        
        # Get image metadata
        metadata = await ImageService.get_image_metadata(file_path)
        
        return {
            'filename': filename,
            'file_path': file_path,
            'file_size': len(content),
            'file_type': file.content_type,
            'metadata': metadata
        }
    
    @staticmethod
    async def get_image_metadata(file_path: str) -> dict:
        """Extract image metadata"""
        try:
            with Image.open(file_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode
                }
        except Exception as e:
            return {
                'width': 0,
                'height': 0,
                'format': 'unknown',
                'mode': 'unknown',
                'error': str(e)
            }
    
    @staticmethod
    async def create_thumbnail(file_path: str, output_dir: str) -> str:
        """Create thumbnail from image"""
        try:
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            thumb_filename = f"{name}_thumb{ext}"
            thumb_path = os.path.join(output_dir, thumb_filename)
            
            os.makedirs(output_dir, exist_ok=True)
            
            with Image.open(file_path) as img:
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode == 'P':
                    img = img.convert('RGB')
                
                img.thumbnail(ImageService.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
                img.save(thumb_path, quality=85, optimize=True)
            
            return thumb_path
        except Exception as e:
            print(f"Error creating thumbnail: {str(e)}")
            return None
    
    @staticmethod
    async def process_image(file_path: str, output_dir: str) -> dict:
        """Process image for AI analysis"""
        try:
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            processed_filename = f"{name}_processed{ext}"
            processed_path = os.path.join(output_dir, processed_filename)
            
            os.makedirs(output_dir, exist_ok=True)
            
            with Image.open(file_path) as img:
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode == 'P':
                    img = img.convert('RGB')
                
                if img.width > ImageService.PROCESSED_SIZE[0] or img.height > ImageService.PROCESSED_SIZE[1]:
                    img.thumbnail(ImageService.PROCESSED_SIZE, Image.Resampling.LANCZOS)
                
                img.save(processed_path, quality=90, optimize=True)
            
            return {
                'processed_path': processed_path,
                'width': img.width,
                'height': img.height
            }
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None
    
    @staticmethod
    def get_file_hash(file_path: str) -> str:
        """Generate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    @staticmethod
    async def cleanup_temp_file(file_path: str):
        """Delete temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {str(e)}")
