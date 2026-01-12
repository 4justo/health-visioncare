import React from 'react';
import { Scan } from '../../api/scans';

interface ScanListProps {
  scans: Scan[];
  onView: (scan: Scan) => void;
  onDelete: (scanId: string) => void;
}

export function ScanList({ scans, onView, onDelete }: ScanListProps) {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-700';
      case 'processing':
        return 'bg-yellow-100 text-yellow-700';
      case 'pending':
        return 'bg-blue-100 text-blue-700';
      case 'failed':
        return 'bg-red-100 text-red-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  if (scans.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No scans found for this patient.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {scans.map((scan) => (
        <div
          key={scan.id}
          className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
        >
          <div className="relative aspect-square bg-gray-100">
            {scan.thumbnail_url ? (
              <img
                src={scan.thumbnail_url}
                alt={scan.file_name}
                className="w-full h-full object-cover cursor-pointer"
                onClick={() => onView(scan)}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                <div className="text-center">
                  <div className="text-4xl mb-2">🖼️</div>
                  <div className="text-sm">No preview</div>
                </div>
              </div>
            )}
            <div className="absolute top-2 right-2">
              <span
                className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                  scan.status
                )}`}
              >
                {scan.status}
              </span>
            </div>
          </div>
          
          <div className="p-4">
            <div className="flex justify-between items-start mb-2">
              <div>
                <h3 className="font-medium text-gray-900">{scan.file_name}</h3>
                <p className="text-sm text-gray-500">{scan.scan_type}</p>
              </div>
              <button
                onClick={() => onDelete(scan.id)}
                className="text-red-500 hover:text-red-700 text-sm"
              >
                Delete
              </button>
            </div>
            
            <div className="text-sm text-gray-600 space-y-1">
              <p>Size: {(scan.file_size / 1024 / 1024).toFixed(2)} MB</p>
              <p>Date: {formatDate(scan.captured_date)}</p>
              {scan.ai_prediction && (
                <p className="font-medium text-blue-600">
                  Prediction: {scan.ai_prediction} ({scan.ai_confidence?.toFixed(2)}%)
                </p>
              )}
            </div>
            
            <button
              onClick={() => onView(scan)}
              className="mt-3 w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
            >
              View Details
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
