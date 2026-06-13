import { Link } from 'react-router-dom'

export const Navbar = ({ rol, onLogout }) => {
  return (
    <nav style={{ background: '#333', padding: '10px', display: 'flex', gap: '16px', alignItems: 'center' }}>
      <span style={{ color: 'white', fontWeight: 'bold' }}>Deportes UCU</span>
      <Link to="/estudiantes" style={{ color: 'white', textDecoration: 'none' }}>Estudiantes</Link>
      <Link to="/actividades" style={{ color: 'white', textDecoration: 'none' }}>Actividades</Link>
      <Link to="/inscripciones" style={{ color: 'white', textDecoration: 'none' }}>Inscripciones</Link>
      <Link to="/asistencias" style={{ color: 'white', textDecoration: 'none' }}>Asistencias</Link>
      <span style={{ color: '#aaa', marginLeft: 'auto' }}>{rol}</span>
      <button onClick={onLogout} style={{ marginLeft: '8px' }}>Salir</button>
    </nav>
  )
}