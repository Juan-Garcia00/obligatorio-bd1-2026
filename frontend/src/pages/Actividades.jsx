import { useEffect, useState } from 'react'

export const Actividades = () => {
  const [actividades, setActividades] = useState([])

  useEffect(() => {
    fetch('http://localhost:5000/actividades')
      .then(res => res.json())
      .then(data => setActividades(data))
  }, [])

  return (
    <div style={{ padding: '20px' }}>
      <h2>Actividades</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Disciplina</th>
            <th>Espacio</th>
            <th>Día</th>
            <th>Hora inicio</th>
            <th>Hora fin</th>
            <th>Cupo</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {actividades.map(a => (
            <tr key={a.id}>
              <td>{a.nombre}</td>
              <td>{a.disciplina_nombre}</td>
              <td>{a.espacio_nombre}</td>
              <td>{a.dia_semana}</td>
              <td>{a.hora_inicio}</td>
              <td>{a.hora_fin}</td>
              <td>{a.cupo_maximo}</td>
              <td>{a.estado}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}