import os
from typing import Optional
import asyncio
from functools import partial
import shutil
from ..core.config import settings

class StorageService:
    def __init__(self):
        self.base_path = settings.UPLOAD_DIR
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(os.path.join(self.base_path, 'scans'), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, 'thumbnails'), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, 'processed'), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, 'temp'), exist_ok=True)
    
    async def upload_file(self, file_path: str, key: str, content_type: str = None) -> str:
        """Upload file to local storage"""
        try:
            if key.startswith('thumbnails/'):
                dest_dir = os.path.join(self.base_path, 'thumbnails')
            elif key.startswith('processed/'):
                dest_dir = os.path.join(self.base_path, 'processed')
            else:
                dest_dir = os.path.join(self.base_path, 'scans')
            
            os.makedirs(dest_dir, exist_ok=True)
            filename = os.path.basename(key)
            dest_path = os.path.join(dest_dir, filename)
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                partial(shutil.copy2, file_path, dest_path)
            )
            
            return f"/uploads/scans/{filename}"
        except Exception as e:
            raise Exception(f"Failed to upload: {str(e)}")
    
    async def delete_file(self, key: str):
        """Delete file from storage"""
        filename = os.path.basename(key)
        file_path = os.path.join(self.base_path, 'scans', filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    async def get_file_url(self, key: str) -> str:
        """Get file URL"""
        return f"/uploads/scans/{os.path.basename(key)}"
