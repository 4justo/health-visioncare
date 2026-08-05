import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { patientApi, Patient } from '../../api/patients';
import { Layout } from '../../components/common/Layout';
import { useAuth } from '../../context/AuthContext';

export function PatientDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(true);
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

  const handleDelete = async () => {
    if (!id || !window.confirm('Are you sure you want to delete this patient?')) return;
    try {
      await patientApi.delete(id);
      navigate('/patients');
    } catch (err) {
      alert('Failed to delete patient');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getAge = (dateOfBirth: string) => {
    const today = new Date();
    const birthDate = new Date(dateOfBirth);
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return age;
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
      <div className="mb-6 flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {patient.first_name} {patient.last_name}
          </h1>
          <p className="text-gray-600 mt-1">Patient ID: {patient.patient_id}</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => navigate(`/patients/${id}/edit`)}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Edit
          </button>
          {user?.role === 'admin' && (
            <button
              onClick={handleDelete}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
            >
              Delete
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Personal Information</h2>
          <dl className="space-y-2">
            <div className="flex justify-between">
              <dt className="text-gray-600">Full Name</dt>
              <dd className="font-medium">{patient.first_name} {patient.last_name}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">Date of Birth</dt>
              <dd className="font-medium">{formatDate(patient.date_of_birth)}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">Age</dt>
              <dd className="font-medium">{getAge(patient.date_of_birth)} years</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">Gender</dt>
              <dd className="font-medium capitalize">{patient.gender}</dd>
            </div>
          </dl>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h2>
          <dl className="space-y-2">
            <div className="flex justify-between">
              <dt className="text-gray-600">Email</dt>
              <dd className="font-medium">{patient.email || '—'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">Phone</dt>
              <dd className="font-medium">{patient.phone || '—'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">Address</dt>
              <dd className="font-medium">{patient.address || '—'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">City/State</dt>
              <dd className="font-medium">
                {patient.city || ''} {patient.state || ''} {patient.zip_code || ''}
              </dd>
            </div>
          </dl>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Medical Information</h2>
          <dl className="space-y-2">
            <div className="flex justify-between">
              <dt className="text-gray-600">Allergies</dt>
              <dd className="font-medium">{patient.allergies || 'None'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">Blood Type</dt>
              <dd className="font-medium">{patient.blood_type || '—'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">Medical History</dt>
              <dd className="font-medium">{patient.medical_history || '—'}</dd>
            </div>
          </dl>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Clinic Information</h2>
          <dl className="space-y-2">
            <div className="flex justify-between">
              <dt className="text-gray-600">Clinic</dt>
              <dd className="font-medium">{patient.clinic_name || '—'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">Primary Physician</dt>
              <dd className="font-medium">{patient.primary_physician || '—'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-600">Referral Source</dt>
              <dd className="font-medium">{patient.referral_source || '—'}</dd>
            </div>
          </dl>
        </div>

        {patient.notes && (
          <div className="md:col-span-2 bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Notes</h2>
            <p className="text-gray-700 whitespace-pre-wrap">{patient.notes}</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
