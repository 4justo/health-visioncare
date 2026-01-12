import { apiClient } from './client';

export interface Scan {
  id: string;
  patient_id: string;
  scan_type: 'retinal' | 'oct' | 'fundus';
  image_url: string;
  thumbnail_url?: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  file_name: string;
  file_size: number;
  file_type: string;
  image_width?: number;
  image_height?: number;
  ai_prediction?: string;
  ai_confidence?: number;
  ai_processing_time?: number;
  ai_model_version?: string;
  ai_results?: any;
  captured_date: string;
  uploaded_by: string;
  processed_date?: string;
  notes?: string;
  heatmap_url?: string;
  overlay_url?: string;
  created_at: string;
}

export interface ScanUploadResponse {
  scan: Scan;
  message: string;
}

export interface ScanListResponse {
  items: Scan[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export const scanApi = {
  upload: async (
    patientId: string,
    scanType: string,
    file: File,
    notes?: string,
    capturedDate?: string
  ): Promise<ScanUploadResponse> => {
    const formData = new FormData();
    formData.append('patient_id', patientId);
    formData.append('scan_type', scanType);
    formData.append('file', file);
    if (notes) formData.append('notes', notes);
    if (capturedDate) formData.append('captured_date', capturedDate);

    const response = await apiClient.post<ScanUploadResponse>(
      '/api/v1/scans/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  getById: async (id: string): Promise<Scan> => {
    const response = await apiClient.get<Scan>(`/api/v1/scans/${id}`);
    return response.data;
  },

  getPatientScans: async (
    patientId: string,
    page: number = 1,
    size: number = 10
  ): Promise<ScanListResponse> => {
    const response = await apiClient.get<ScanListResponse>(
      `/api/v1/scans/patient/${patientId}`,
      { params: { page, size } }
    );
    return response.data;
  },

  update: async (id: string, data: any): Promise<Scan> => {
    const response = await apiClient.put<Scan>(`/api/v1/scans/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/v1/scans/${id}`);
  },
};
