import { useEffect, useState } from "react";

const API = "http://localhost:5000";

export const Estudiantes = ({ rol }) => {
  const [estudiantes, setEstudiantes] = useState([]);
  const [carreras, setCarreras] = useState([]);
  const [facultades, setFacultades] = useState([]);
  const [form, setForm] = useState({
    documento: "",
    nombre: "",
    apellido: "",
    email: "",
    carrera_id: "",
    facultad_id: "",
  });
  const [editId, setEditId] = useState(null);
  const [error, setError] = useState("");

  const headers = { "Content-Type": "application/json", "X-Rol": rol };

  const cargar = () => {
    fetch(`${API}/estudiantes`, { headers })
      .then((r) => r.json())
      .then(setEstudiantes);
    fetch(`${API}/carreras`, { headers })
      .then((r) => r.json())
      .then(setCarreras);
    fetch(`${API}/facultades`, { headers })
      .then((r) => r.json())
      .then(setFacultades);
  };

  useEffect(() => {
    cargar();
  }, []);

  const limpiar = () => {
    setForm({
      documento: "",
      nombre: "",
      apellido: "",
      email: "",
      carrera_id: "",
      facultad_id: "",
    });
    setEditId(null);
    setError("");
  };

  const guardar = () => {
    if (
      !form.documento ||
      !form.nombre ||
      !form.apellido ||
      !form.email ||
      !form.carrera_id ||
      !form.facultad_id
    ) {
      setError("Todos los campos son obligatorios");
      return;
    }
    const url = editId ? `${API}/estudiantes/${editId}` : `${API}/estudiantes`;
    const method = editId ? "PUT" : "POST";
    fetch(url, { method, headers, body: JSON.stringify(form) })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          return;
        }
        limpiar();
        cargar();
      });
  };

  const editar = (e) => {
    setEditId(e.id);
    setForm({
      documento: e.documento,
      nombre: e.nombre,
      apellido: e.apellido,
      email: e.email,
      carrera_id: e.carrera_id,
      facultad_id: e.facultad_id,
    });
    setError("");
  };

  const eliminar = (id) => {
    if (!confirm("¿Eliminar estudiante?")) return;
    fetch(`${API}/estudiantes/${id}`, { method: "DELETE", headers })
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
      <h2>Estudiantes</h2>

      {rol === "ADMIN" && (
        <div
          style={{
            marginBottom: "20px",
            padding: "16px",
            border: "1px solid #ccc",
            borderRadius: "6px",
            maxWidth: "500px",
          }}
        >
          <h3 style={{ marginTop: 0 }}>
            {editId ? "Editar estudiante" : "Nuevo estudiante"}
          </h3>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <input
              placeholder="Documento"
              value={form.documento}
              onChange={(e) => setForm({ ...form, documento: e.target.value })}
            />
            <input
              placeholder="Nombre"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            />
            <input
              placeholder="Apellido"
              value={form.apellido}
              onChange={(e) => setForm({ ...form, apellido: e.target.value })}
            />
            <input
              placeholder="Email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
            <select
              value={form.carrera_id}
              onChange={(e) => setForm({ ...form, carrera_id: e.target.value })}
            >
              <option value="">-- Carrera --</option>
              {carreras.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.nombre}
                </option>
              ))}
            </select>
            <select
              value={form.facultad_id}
              onChange={(e) =>
                setForm({ ...form, facultad_id: e.target.value })
              }
            >
              <option value="">-- Facultad --</option>
              {facultades.map((f) => (
                <option key={f.id} value={f.id}>
                  {f.nombre}
                </option>
              ))}
            </select>
            <div style={{ display: "flex", gap: "8px" }}>
              <button onClick={guardar}>
                {editId ? "Guardar cambios" : "Crear"}
              </button>
              {editId && <button onClick={limpiar}>Cancelar</button>}
            </div>
          </div>
        </div>
      )}

      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Documento</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Email</th>
            {rol === "ADMIN" && <th>Acciones</th>}
          </tr>
        </thead>
        <tbody>
          {estudiantes.map((e) => (
            <tr key={e.id}>
              <td>{e.documento}</td>
              <td>{e.nombre}</td>
              <td>{e.apellido}</td>
              <td>{e.email}</td>
              {rol === "ADMIN" && (
                <td>
                  <button onClick={() => editar(e)}>Editar</button>{" "}
                  <button
                    onClick={() => eliminar(e.id)}
                    style={{ color: "red" }}
                  >
                    Eliminar
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
