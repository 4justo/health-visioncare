import { apiClient } from './client';

export interface Patient {
  id: string;
  patient_id: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'male' | 'female' | 'other';
  age?: number;
  
  email?: string;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  
  blood_type?: 'A+' | 'A-' | 'B+' | 'B-' | 'AB+' | 'AB-' | 'O+' | 'O-';
  allergies?: string;
  medical_history?: string;
  current_medications?: string;
  
  clinic_name?: string;
  clinic_address?: string;
  primary_physician?: string;
  referral_source?: string;
  
  is_active: boolean;
  is_deceased: boolean;
  created_at: string;
  updated_at?: string;
  last_visit_date?: string;
  next_appointment?: string;
  created_by: string;
  notes?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  emergency_contact_relation?: string;
}

export interface PatientCreate {
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'male' | 'female' | 'other';
  email?: string;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  blood_type?: 'A+' | 'A-' | 'B+' | 'B-' | 'AB+' | 'AB-' | 'O+' | 'O-';
  allergies?: string;
  medical_history?: string;
  current_medications?: string;
  clinic_name?: string;
  clinic_address?: string;
  primary_physician?: string;
  referral_source?: string;
  notes?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  emergency_contact_relation?: string;
}

export interface PatientUpdate extends Partial<PatientCreate> {
  is_active?: boolean;
  is_deceased?: boolean;
}

export interface PatientListResponse {
  items: Patient[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface PatientStats {
  total: number;
  gender_distribution: {
    male: number;
    female: number;
    other: number;
  };
  age_groups: {
    '0-18': number;
    '19-35': number;
    '36-50': number;
    '51-65': number;
    '65+': number;
  };
  recent_patients: number;
  clinic_count: number;
}

export const patientApi = {
  create: async (data: PatientCreate): Promise<Patient> => {
    const response = await apiClient.post<Patient>('/api/v1/patients/', data);
    return response.data;
  },

  getById: async (id: string): Promise<Patient> => {
    const response = await apiClient.get<Patient>(`/api/v1/patients/${id}`);
    return response.data;
  },

  getByPatientId: async (patientId: string): Promise<Patient> => {
    const response = await apiClient.get<Patient>(`/api/v1/patients/by-patient-id/${patientId}`);
    return response.data;
  },

  update: async (id: string, data: PatientUpdate): Promise<Patient> => {
    const response = await apiClient.put<Patient>(`/api/v1/patients/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/v1/patients/${id}`);
  },

  hardDelete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/v1/patients/${id}/hard`);
  },

  search: async (params: {
    search?: string;
    gender?: string;
    is_active?: boolean;
    clinic_name?: string;
    created_after?: string;
    created_before?: string;
    page?: number;
    size?: number;
    sort_by?: string;
    sort_order?: string;
  }): Promise<PatientListResponse> => {
    const response = await apiClient.get<PatientListResponse>('/api/v1/patients/', { params });
    return response.data;
  },

  getStats: async (): Promise<PatientStats> => {
    const response = await apiClient.get<PatientStats>('/api/v1/patients/stats');
    return response.data;
  },

  getRecent: async (limit: number = 10): Promise<Patient[]> => {
    const response = await apiClient.get<Patient[]>('/api/v1/patients/recent/', {
      params: { limit }
    });
    return response.data;
  },

  getHistory: async (id: string): Promise<any> => {
    const response = await apiClient.get(`/api/v1/patients/${id}/history`);
    return response.data;
  }
};
