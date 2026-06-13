import { useEffect, useState } from "react";

const API = "http://localhost:5000";

export const Espacios = ({ rol }) => {
  const [espacios, setEspacios] = useState([]);
  const [form, setForm] = useState({
    nombre: "",
    ubicacion: "",
    capacidad: "",
  });
  const [editId, setEditId] = useState(null);
  const [error, setError] = useState("");

  const headers = { "Content-Type": "application/json", "X-Rol": rol };

  const cargar = () =>
    fetch(`${API}/espacios`, { headers })
      .then((r) => r.json())
      .then(setEspacios);

  useEffect(() => {
    cargar();
  }, []);

  const limpiar = () => {
    setForm({ nombre: "", ubicacion: "", capacidad: "" });
    setEditId(null);
    setError("");
  };

  const guardar = () => {
    if (!form.nombre || !form.ubicacion || !form.capacidad) {
      setError("Todos los campos son obligatorios");
      return;
    }
    const url = editId ? `${API}/espacios/${editId}` : `${API}/espacios`;
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

  const eliminar = (id) => {
    if (!confirm("¿Eliminar espacio?")) return;
    fetch(`${API}/espacios/${id}`, { method: "DELETE", headers })
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
      <h2>Espacios deportivos</h2>
      <div
        style={{
          marginBottom: "20px",
          padding: "16px",
          border: "1px solid #ccc",
          borderRadius: "6px",
          maxWidth: "400px",
        }}
      >
        <h3 style={{ marginTop: 0 }}>
          {editId ? "Editar espacio" : "Nuevo espacio"}
        </h3>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          <input
            placeholder="Nombre"
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
          />
          <input
            placeholder="Ubicación"
            value={form.ubicacion}
            onChange={(e) => setForm({ ...form, ubicacion: e.target.value })}
          />
          <input
            placeholder="Capacidad"
            type="number"
            value={form.capacidad}
            onChange={(e) => setForm({ ...form, capacidad: e.target.value })}
          />
          <div style={{ display: "flex", gap: "8px" }}>
            <button onClick={guardar}>
              {editId ? "Guardar cambios" : "Crear"}
            </button>
            {editId && <button onClick={limpiar}>Cancelar</button>}
          </div>
        </div>
      </div>

      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Ubicación</th>
            <th>Capacidad</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {espacios.map((e) => (
            <tr key={e.id}>
              <td>{e.nombre}</td>
              <td>{e.ubicacion}</td>
              <td>{e.capacidad}</td>
              <td>
                <button
                  onClick={() => {
                    setEditId(e.id);
                    setForm({
                      nombre: e.nombre,
                      ubicacion: e.ubicacion,
                      capacidad: e.capacidad,
                    });
                    setError("");
                  }}
                >
                  Editar
                </button>{" "}
                <button onClick={() => eliminar(e.id)} style={{ color: "red" }}>
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
