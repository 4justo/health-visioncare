import React from 'react';
import { useNavigate } from 'react-router-dom';
import { PatientList } from '../../components/patients/PatientList';
import { Layout } from '../../components/common/Layout';
import { Patient } from '../../api/patients';

export function PatientListPage() {
  const navigate = useNavigate();

  const handleView = (patient: Patient) => {
    navigate(`/patients/${patient.id}`);
  };

  const handleEdit = (patient: Patient) => {
    navigate(`/patients/${patient.id}/edit`);
  };

  return (
    <Layout>
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Patients</h1>
          <p className="text-gray-600 mt-1">Manage your patient records</p>
        </div>
        <button
          onClick={() => navigate('/patients/create')}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Add New Patient
        </button>
      </div>

      <PatientList onView={handleView} onEdit={handleEdit} />
    </Layout>
  );
}
