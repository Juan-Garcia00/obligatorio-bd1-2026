import { useEffect, useState } from 'react'

export const Asistencias = () => {
  const [asistencias, setAsistencias] = useState([])

  useEffect(() => {
    fetch('http://localhost:5000/asistencias')
      .then(res => res.json())
      .then(data => setAsistencias(data))
  }, [])

  return (
    <div style={{ padding: '20px' }}>
      <h2>Asistencias</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Estudiante</th>
            <th>Actividad</th>
            <th>Fecha</th>
            <th>Presente</th>
          </tr>
        </thead>
        <tbody>
          {asistencias.map(a => (
            <tr key={a.id}>
              <td>{a.estudiante_nombre} {a.estudiante_apellido}</td>
              <td>{a.actividad_nombre}</td>
              <td>{a.fecha}</td>
              <td>{a.presente ? 'Sí' : 'No'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}