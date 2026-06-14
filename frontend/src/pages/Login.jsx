import { useState } from 'react'
 
export const Login = ({ onLogin }) => {
  const [rol, setRol] = useState('')
 
  const handleSubmit = () => {
    if (!rol) return
    onLogin(rol)
  }
 
  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#1a1a2e',
      }}
    >
      <div
        style={{
          background: '#fff',
          borderRadius: '8px',
          padding: '40px',
          width: '100%',
          maxWidth: '380px',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.25)',
          textAlign: 'center',
        }}
      >
        <div style={{ fontSize: '36px', marginBottom: '8px' }}>🏋️</div>
        <h2 style={{ margin: '0 0 4px', color: '#1a1a2e' }}>
          Gestión de Actividades Deportivas
        </h2>
        <p style={{ color: '#666', fontSize: '14px', marginTop: '4px', marginBottom: '28px' }}>
          Seleccioná tu rol para continuar
        </p>
 
        <div style={{ textAlign: 'left', marginBottom: '20px' }}>
          <label
            style={{
              display: 'block',
              marginBottom: '6px',
              fontSize: '13px',
              fontWeight: 'bold',
              color: '#1a1a2e',
            }}
          >
            Rol
          </label>
          <select
            value={rol}
            onChange={e => setRol(e.target.value)}
            style={{
              width: '100%',
              padding: '10px',
              borderRadius: '4px',
              border: '1px solid #ccc',
              fontSize: '14px',
              color: '#1a1a2e',
              background: '#fff',
            }}
          >
            <option value="">-- Seleccionar --</option>
            <option value="ADMIN">Admin</option>
            <option value="DOCENTE">Docente</option>
            <option value="ESTUDIANTE">Estudiante</option>
          </select>
        </div>
 
        <button
          onClick={handleSubmit}
          disabled={!rol}
          style={{
            width: '100%',
            background: rol ? '#1a1a2e' : '#ccc',
            color: '#fff',
            border: 'none',
            padding: '12px',
            borderRadius: '4px',
            fontSize: '14px',
            fontWeight: 'bold',
            cursor: rol ? 'pointer' : 'not-allowed',
          }}
        >
          Entrar
        </button>
      </div>
    </div>
  )
}