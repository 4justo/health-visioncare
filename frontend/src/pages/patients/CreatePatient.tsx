import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { patientApi, PatientCreate } from '../../api/patients';
import { PatientForm } from '../../components/patients/PatientForm';
import { Layout } from '../../components/common/Layout';

export function CreatePatient() {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (data: PatientCreate) => {
    setIsSubmitting(true);
    setError('');
    try {
      await patientApi.create(data);
      navigate('/patients');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create patient');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Create New Patient</h1>
        <p className="text-gray-600 mt-1">Add a new patient to the system</p>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          {error}
        </div>
      )}

      <PatientForm
        onSubmit={handleSubmit}
        onCancel={() => navigate('/patients')}
        isSubmitting={isSubmitting}
      />
    </Layout>
  );
}
