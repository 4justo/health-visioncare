import React, { useState, useCallback, useRef } from 'react';
import { scanApi } from '../../api/scans';

interface DragDropUploadProps {
  patientId: string;
  scanType: 'retinal' | 'oct' | 'fundus';
  onUploadSuccess: (scan: any) => void;
  onUploadError: (error: string) => void;
}

export function DragDropUpload({
  patientId,
  scanType,
  onUploadSuccess,
  onUploadError,
}: DragDropUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    async (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        await handleFileUpload(files[0]);
      }
    },
    [patientId, scanType]
  );

  const handleFileInput = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        await handleFileUpload(files[0]);
      }
    },
    [patientId, scanType]
  );

  const handleFileUpload = async (file: File) => {
    // Validate file
    const validTypes = ['image/jpeg', 'image/png', 'image/tiff', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
      onUploadError('Invalid file type. Please upload JPEG, PNG, TIFF, or BMP images.');
      return;
    }

    const maxSize = 50 * 1024 * 1024; // 50MB
    if (file.size > maxSize) {
      onUploadError('File size exceeds 50MB limit.');
      return;
    }

    // Create preview
    const reader = new FileReader();
    reader.onload = () => {
      setPreviewUrl(reader.result as string);
    };
    reader.readAsDataURL(file);

    setIsUploading(true);
    setProgress(0);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const response = await scanApi.upload(
        patientId,
        scanType,
        file,
        undefined,
        new Date().toISOString()
      );

      clearInterval(progressInterval);
      setProgress(100);
      
      setTimeout(() => {
        setIsUploading(false);
        setProgress(0);
        setPreviewUrl(null);
        onUploadSuccess(response.scan);
      }, 500);
      
    } catch (error: any) {
      setIsUploading(false);
      setProgress(0);
      onUploadError(error.response?.data?.detail || 'Failed to upload scan');
    }
  };

  return (
    <div className="space-y-4">
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        } ${isUploading ? 'opacity-50 pointer-events-none' : ''}`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/tiff,image/bmp"
          onChange={handleFileInput}
          className="hidden"
          disabled={isUploading}
        />

        {previewUrl ? (
          <div className="space-y-4">
            <img
              src={previewUrl}
              alt="Preview"
              className="max-h-64 mx-auto rounded-lg"
            />
            {isUploading && (
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            )}
            <p className="text-sm text-gray-600">
              {isUploading ? `Uploading... ${progress}%` : 'Click or drop to replace'}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-6xl">📤</div>
            <div>
              <p className="text-lg font-medium text-gray-700">
                Drag and drop your image here
              </p>
              <p className="text-sm text-gray-500 mt-1">
                or click to browse files
              </p>
            </div>
            <div className="text-xs text-gray-400">
              Supports: JPEG, PNG, TIFF, BMP (Max 50MB)
            </div>
          </div>
        )}
      </div>

      {isUploading && (
        <div className="text-center text-sm text-gray-600">
          <p>Uploading scan... Please wait</p>
        </div>
      )}
    </div>
  );
}
