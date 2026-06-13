import { useState } from 'react'

export const Login = ({ onLogin }) => {
  const [rol, setRol] = useState('')

  const handleSubmit = () => {
    if (!rol) return
    onLogin(rol)
  }

  return (
    <div style={{ padding: '40px' }}>
      <h2>Iniciar sesión</h2>
      <br />
      <label>Seleccioná tu rol:</label>
      <br /><br />
      <select value={rol} onChange={e => setRol(e.target.value)}>
        <option value="">-- Seleccionar --</option>
        <option value="ADMIN">Admin</option>
        <option value="DOCENTE">Docente</option>
        <option value="ESTUDIANTE">Estudiante</option>
      </select>
      <br /><br />
      <button onClick={handleSubmit}>Entrar</button>
    </div>
  )
}