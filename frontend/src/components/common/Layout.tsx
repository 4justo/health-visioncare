import React, { ReactNode } from 'react'
import { Link } from 'react-router-dom'

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/dashboard" className="text-xl font-semibold text-gray-900">
            VisionCare
          </Link>
          <nav className="space-x-4 text-sm text-gray-600">
            <Link to="/dashboard" className="hover:text-gray-900">
              Dashboard
            </Link>
            <Link to="/patients" className="hover:text-gray-900">
              Patients
            </Link>
          </nav>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
    </div>
  )
}
