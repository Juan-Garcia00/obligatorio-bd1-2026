import { useEffect, useState } from "react";

const API = "http://localhost:5000";

export const Asistencias = ({ rol }) => {
  const [asistencias, setAsistencias] = useState([]);
  const [actividades, setActividades] = useState([]);
  const [form, setForm] = useState({
    estudiante_id: "",
    actividad_id: "",
    fecha: "",
    presente: true,
  });
  const [error, setError] = useState("");

  const headers = { "Content-Type": "application/json", "X-Rol": rol };

  const cargar = () => {
    fetch(`${API}/asistencias`, { headers })
      .then((r) => r.json())
      .then(setAsistencias);
    fetch(`${API}/actividades`, { headers })
      .then((r) => r.json())
      .then(setActividades);
  };

  useEffect(() => {
    cargar();
  }, []);

  const registrar = () => {
    if (!form.estudiante_id || !form.actividad_id || !form.fecha) {
      setError("Todos los campos son obligatorios");
      return;
    }
    fetch(`${API}/asistencias`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        ...form,
        estudiante_id: parseInt(form.estudiante_id),
        actividad_id: parseInt(form.actividad_id),
      }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          return;
        }
        setForm({
          estudiante_id: "",
          actividad_id: "",
          fecha: "",
          presente: true,
        });
        setError("");
        cargar();
      });
  };

  return (
    <div>
      <h2>Asistencias</h2>

      {(rol === "ADMIN" || rol === "DOCENTE") && (
        <div
          style={{
            marginBottom: "20px",
            padding: "16px",
            border: "1px solid #ccc",
            borderRadius: "6px",
            maxWidth: "400px",
          }}
        >
          <h3 style={{ marginTop: 0 }}>Registrar asistencia</h3>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <input
              placeholder="ID Estudiante"
              type="number"
              value={form.estudiante_id}
              onChange={(e) =>
                setForm({ ...form, estudiante_id: e.target.value })
              }
            />
            <select
              value={form.actividad_id}
              onChange={(e) =>
                setForm({ ...form, actividad_id: e.target.value })
              }
            >
              <option value="">-- Actividad --</option>
              {actividades.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.nombre}
                </option>
              ))}
            </select>
            <input
              type="date"
              value={form.fecha}
              onChange={(e) => setForm({ ...form, fecha: e.target.value })}
            />
            <label>
              <input
                type="checkbox"
                checked={form.presente}
                onChange={(e) =>
                  setForm({ ...form, presente: e.target.checked })
                }
              />{" "}
              Presente
            </label>
            <button onClick={registrar}>Registrar</button>
          </div>
        </div>
      )}

      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Estudiante</th>
            <th>Actividad</th>
            <th>Fecha</th>
            <th>Presente</th>
          </tr>
        </thead>
        <tbody>
          {asistencias.map((a) => (
            <tr key={a.id}>
              <td>
                {a.estudiante_nombre} {a.estudiante_apellido}
              </td>
              <td>{a.actividad_nombre}</td>
              <td>{a.fecha}</td>
              <td>{a.presente ? "✅" : "❌"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
