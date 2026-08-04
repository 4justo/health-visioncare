import { apiClient } from './client';

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  role: 'admin' | 'doctor' | 'technician';
  is_active: boolean;
  is_verified: boolean;
  last_login: string | null;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  full_name: string;
  password: string;
  role?: 'admin' | 'doctor' | 'technician';
}

export interface TokenRefreshResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
}

export const authApi = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/api/v1/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<User> => {
    const response = await apiClient.post<User>('/api/v1/auth/register', data);
    return response.data;
  },

  logout: async (refreshToken: string): Promise<void> => {
    await apiClient.post('/api/v1/auth/logout', null, {
      params: { refresh_token: refreshToken },
    });
  },

  refreshToken: async (refreshToken: string): Promise<TokenRefreshResponse> => {
    const response = await apiClient.post<TokenRefreshResponse>('/api/v1/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/api/v1/auth/me');
    return response.data;
  },

  updateUser: async (data: Partial<User>): Promise<User> => {
    const response = await apiClient.put<User>('/api/v1/auth/me', data);
    return response.data;
  },

  changePassword: async (data: ChangePasswordRequest): Promise<void> => {
    await apiClient.post('/api/v1/auth/change-password', data);
  },

  getUsers: async (skip: number = 0, limit: number = 100): Promise<User[]> => {
    const response = await apiClient.get<User[]>('/api/v1/auth/users', {
      params: { skip, limit },
    });
    return response.data;
  },

  getUserById: async (userId: string): Promise<User> => {
    const response = await apiClient.get<User>(`/api/v1/auth/users/${userId}`);
    return response.data;
  },

  updateUserById: async (userId: string, data: Partial<User>): Promise<User> => {
    const response = await apiClient.put<User>(`/api/v1/auth/users/${userId}`, data);
    return response.data;
  },

  deleteUser: async (userId: string): Promise<void> => {
    await apiClient.delete(`/api/v1/auth/users/${userId}`);
  },
};
