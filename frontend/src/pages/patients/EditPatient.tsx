import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { patientApi, Patient, PatientUpdate } from '../../api/patients';
import { PatientForm } from '../../components/patients/PatientForm';
import { Layout } from '../../components/common/Layout';

export function EditPatient() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      loadPatient(id);
    }
  }, [id]);

  const loadPatient = async (patientId: string) => {
    try {
      const data = await patientApi.getById(patientId);
      setPatient(data);
    } catch (err) {
      setError('Failed to load patient');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (data: PatientUpdate) => {
    if (!id) return;
    setIsSubmitting(true);
    setError('');
    try {
      await patientApi.update(id, data);
      navigate(`/patients/${id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update patient');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center py-8">
          <div className="text-gray-500">Loading patient...</div>
        </div>
      </Layout>
    );
  }

  if (!patient) {
    return (
      <Layout>
        <div className="text-center py-8 text-red-600">Patient not found</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Edit Patient</h1>
        <p className="text-gray-600 mt-1">
          Editing {patient.first_name} {patient.last_name}
        </p>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          {error}
        </div>
      )}

      <PatientForm
        patient={patient}
        onSubmit={handleSubmit}
        onCancel={() => navigate(`/patients/${id}`)}
        isSubmitting={isSubmitting}
      />
    </Layout>
  );
}
