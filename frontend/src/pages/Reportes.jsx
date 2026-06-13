import { useEffect, useState } from "react";

const API = "http://localhost:5000";

const REPORTES = [
  {
    key: "mas-confirmados",
    label: "1. Actividades con más inscriptos confirmados",
  },
  { key: "cupos-disponibles", label: "2. Actividades con cupos disponibles" },
  { key: "inscriptos-disciplina", label: "3. Inscriptos por disciplina" },
  {
    key: "inscriptos-carrera-facultad",
    label: "4. Inscriptos por carrera y facultad",
  },
  { key: "ocupacion", label: "5. Porcentaje de ocupación por actividad" },
  { key: "asistencia", label: "6. Porcentaje de asistencia por actividad" },
  { key: "inasistencias", label: "7. Estudiantes con 3 o más inasistencias" },
  { key: "lista-espera", label: "8. Estudiantes en lista de espera" },
  { key: "espacios-utilizados", label: "9. Espacios más utilizados" },
  { key: "inscripciones-por-estado", label: "10. Inscripciones por estado" },
];

export const Reportes = ({ rol }) => {
  const [seleccionado, setSeleccionado] = useState(null);
  const [datos, setDatos] = useState([]);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  const headers = { "X-Rol": rol };

  const cargarReporte = (key) => {
    setSeleccionado(key);
    setCargando(true);
    setDatos([]);
    setError("");
    fetch(`${API}/reportes/${key}`, { headers })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          setCargando(false);
          return;
        }
        setDatos(data);
        setCargando(false);
      })
      .catch(() => {
        setError("Error al conectar con el servidor");
        setCargando(false);
      });
  };

  const columnas = datos.length > 0 ? Object.keys(datos[0]) : [];

  return (
    <div>
      <h2>Reportes</h2>
      <div
        style={{
          display: "flex",
          gap: "8px",
          flexWrap: "wrap",
          marginBottom: "20px",
        }}
      >
        {REPORTES.map((r) => (
          <button
            key={r.key}
            onClick={() => cargarReporte(r.key)}
            style={{
              padding: "8px 12px",
              background: seleccionado === r.key ? "#1a1a2e" : "#eee",
              color: seleccionado === r.key ? "#fff" : "#000",
              border: "1px solid #ccc",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            {r.label}
          </button>
        ))}
      </div>

      {cargando && <p>Cargando...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!cargando && !error && datos.length > 0 && (
        <table
          border="1"
          cellPadding="8"
          style={{ borderCollapse: "collapse" }}
        >
          <thead>
            <tr>
              {columnas.map((c) => (
                <th key={c}>{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {datos.map((fila, i) => (
              <tr key={i}>
                {columnas.map((c) => (
                  <td key={c}>{fila[c]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!cargando && !error && seleccionado && datos.length === 0 && (
        <p>No hay datos para mostrar.</p>
      )}
    </div>
  );
};
