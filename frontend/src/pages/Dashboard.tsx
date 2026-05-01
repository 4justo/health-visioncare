import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Layout } from '../components/common/Layout';

export function Dashboard() {
  const { user } = useAuth();

  return (
    <Layout>
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Welcome, {user?.full_name}!
        </h1>
        <p className="text-gray-600">
          Role: <span className="font-medium capitalize">{user?.role}</span>
        </p>
        <p className="text-gray-600">
          Email: <span className="font-medium">{user?.email}</span>
        </p>
        <div className="mt-6 p-4 bg-blue-50 rounded-md">
          <p className="text-blue-700">
            🎉 Authentication is working! This is a protected dashboard.
          </p>
        </div>
      </div>
    </Layout>
  );
}
