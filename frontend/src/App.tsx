import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { HealthCheck } from './pages/HealthCheck';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Unauthorized } from './pages/Unauthorized';
import { PatientListPage } from './pages/patients/PatientListPage';
import { CreatePatient } from './pages/patients/CreatePatient';
import { EditPatient } from './pages/patients/EditPatient';
import { PatientDetail } from './pages/patients/PatientDetail';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<HealthCheck />} />
          <Route path="/health" element={<HealthCheck />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/unauthorized" element={<Unauthorized />} />
          
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patients"
            element={
              <ProtectedRoute allowedRoles={['admin', 'doctor', 'technician']}>
                <PatientListPage />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patients/create"
            element={
              <ProtectedRoute allowedRoles={['admin', 'doctor', 'technician']}>
                <CreatePatient />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patients/:id"
            element={
              <ProtectedRoute allowedRoles={['admin', 'doctor', 'technician']}>
                <PatientDetail />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/patients/:id/edit"
            element={
              <ProtectedRoute allowedRoles={['admin', 'doctor', 'technician']}>
                <EditPatient />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                  <div className="bg-white p-8 rounded-lg shadow-md">
                    <h1 className="text-2xl font-bold">Admin Panel</h1>
                    <p className="text-gray-600 mt-2">Only admins can see this page.</p>
                  </div>
                </div>
              </ProtectedRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
