import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Navbar } from './components/Navbar'
import { Estudiantes } from './pages/Estudiantes'
import { Actividades } from './pages/Actividades'
import { Inscripciones } from './pages/Inscripciones'
import { Asistencias } from './pages/Asistencias'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/estudiantes" element={<Estudiantes />} />
        <Route path="/actividades" element={<Actividades />} />
        <Route path="/inscripciones" element={<Inscripciones />} />
        <Route path="/asistencias" element={<Asistencias />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App