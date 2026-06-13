import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Navbar } from './components/Navbar'
import { Login } from './pages/Login'
import { Estudiantes } from './pages/Estudiantes'
import { Actividades } from './pages/Actividades'
import { Inscripciones } from './pages/Inscripciones'
import { Asistencias } from './pages/Asistencias'
import './App.css'

function App() {
  const [rol, setRol] = useState(null)

  if (!rol) return <Login onLogin={setRol} />

  return (
    <BrowserRouter>
      <Navbar rol={rol} onLogout={() => setRol(null)} />
      <Routes>
        <Route path="/estudiantes" element={<Estudiantes rol={rol} />} />
        <Route path="/actividades" element={<Actividades rol={rol} />} />
        <Route path="/inscripciones" element={<Inscripciones rol={rol} />} />
        <Route path="/asistencias" element={<Asistencias rol={rol} />} />
        <Route path="*" element={<Navigate to="/estudiantes" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App