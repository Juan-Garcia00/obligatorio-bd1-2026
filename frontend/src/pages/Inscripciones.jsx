import { useEffect, useState } from "react";

const API = "http://localhost:5000";

export const Inscripciones = ({ rol }) => {
  const [inscripciones, setInscripciones] = useState([]);

  const headers = { "Content-Type": "application/json", "X-Rol": rol };

  const cargar = () =>
    fetch(`${API}/inscripciones`, { headers })
      .then((r) => r.json())
      .then(setInscripciones);

  useEffect(() => {
    cargar();
  }, []);

  const cancelar = (id) => {
    if (!confirm("¿Cancelar inscripción?")) return;
    fetch(`${API}/inscripciones/${id}`, { method: "DELETE", headers })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          return;
        }
        cargar();
      });
  };

  return (
    <div>
      <h2>Inscripciones</h2>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Estudiante</th>
            <th>Actividad</th>
            <th>Estado</th>
            <th>Fecha</th>
            {(rol === "ADMIN" || rol === "ESTUDIANTE") && <th>Acciones</th>}
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
              {(rol === "ADMIN" || rol === "ESTUDIANTE") && (
                <td>
                  <button
                    onClick={() => cancelar(i.id)}
                    style={{ color: "red" }}
                  >
                    Cancelar
                  </button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
