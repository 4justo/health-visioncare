import React, { useState, useEffect } from 'react'
import { healthApi } from '../api/health'

export function HealthCheck() {
  const [apiStatus, setApiStatus] = useState<string>('Checking...')
  const [dbStatus, setDbStatus] = useState<string>('Checking...')
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const api = await healthApi.check()
        setApiStatus(api.status)

        const db = await healthApi.dbCheck()
        setDbStatus(db.database || 'connected')
      } catch (error) {
        setApiStatus('unhealthy')
        setDbStatus('disconnected')
      } finally {
        setLoading(false)
      }
    }

    checkHealth()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full">
        <h1 className="text-2xl font-bold mb-6 text-center">VisionCare</h1>
        <div className="space-y-4">
          <div className="flex justify-between items-center border-b pb-2">
            <span className="font-medium">API Status:</span>
            <span className={`px-3 py-1 rounded-full text-sm ${
              apiStatus === 'healthy' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
            }`}>
              {apiStatus}
            </span>
          </div>
          <div className="flex justify-between items-center border-b pb-2">
            <span className="font-medium">Database:</span>
            <span className={`px-3 py-1 rounded-full text-sm ${
              dbStatus === 'connected' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
            }`}>
              {dbStatus}
            </span>
          </div>
          <div className="mt-6 text-center text-sm text-gray-500">
            VisionCare v0.1.0
          </div>
        </div>
      </div>
    </div>
  )
}