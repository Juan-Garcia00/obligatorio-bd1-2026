import { useEffect, useState } from "react";

export const Inscripciones = ({ rol }) => {
  const [inscripciones, setInscripciones] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/inscripciones", {
      headers: { "X-Rol": rol },
    })
      .then((res) => res.json())
      .then((data) => setInscripciones(data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Inscripciones</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Estudiante</th>
            <th>Actividad</th>
            <th>Estado</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {inscripciones.map((i) => (
            <tr key={i.id}>
              <td>
                {i.estudiante_nombre} {i.estudiante_apellido}
              </td>
              <td>{i.actividad_nombre}</td>
              <td>{i.estado}</td>
              <td>{i.fecha_inscripcion}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
