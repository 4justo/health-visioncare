import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { HealthCheck } from './pages/HealthCheck'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HealthCheck />} />
        <Route path="/health" element={<HealthCheck />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App