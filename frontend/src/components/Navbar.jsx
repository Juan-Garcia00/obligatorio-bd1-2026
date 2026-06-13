import { Link } from 'react-router-dom'

export const Navbar = () => {
  return (
    <nav style={{ background: '#333', padding: '10px', display: 'flex', gap: '16px' }}>
      <span style={{ color: 'white', fontWeight: 'bold' }}>Deportes UCU</span>
      <Link to="/estudiantes" style={{ color: 'white', textDecoration: 'none' }}>Estudiantes</Link>
      <Link to="/actividades" style={{ color: 'white', textDecoration: 'none' }}>Actividades</Link>
      <Link to="/inscripciones" style={{ color: 'white', textDecoration: 'none' }}>Inscripciones</Link>
      <Link to="/asistencias" style={{ color: 'white', textDecoration: 'none' }}>Asistencias</Link>
    </nav>
  )
}