import { useEffect, useState } from "react";

const API = "http://localhost:5000";

export const Disciplinas = ({ rol }) => {
  const [disciplinas, setDisciplinas] = useState([]);
  const [form, setForm] = useState({ nombre: "", descripcion: "" });
  const [editId, setEditId] = useState(null);
  const [error, setError] = useState("");

  const headers = { "Content-Type": "application/json", "X-Rol": rol };

  const cargar = () =>
    fetch(`${API}/disciplinas`, { headers })
      .then((r) => r.json())
      .then(setDisciplinas);

  useEffect(() => {
    cargar();
  }, []);

  const limpiar = () => {
    setForm({ nombre: "", descripcion: "" });
    setEditId(null);
    setError("");
  };

  const guardar = () => {
    if (!form.nombre) {
      setError("El nombre es obligatorio");
      return;
    }
    const url = editId ? `${API}/disciplinas/${editId}` : `${API}/disciplinas`;
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
    if (!confirm("¿Eliminar disciplina?")) return;
    fetch(`${API}/disciplinas/${id}`, { method: "DELETE", headers })
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
      <h2>Disciplinas</h2>
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
          {editId ? "Editar disciplina" : "Nueva disciplina"}
        </h3>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          <input
            placeholder="Nombre"
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
          />
          <input
            placeholder="Descripción (opcional)"
            value={form.descripcion}
            onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
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
            <th>Descripción</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {disciplinas.map((d) => (
            <tr key={d.id}>
              <td>{d.nombre}</td>
              <td>{d.descripcion}</td>
              <td>
                <button
                  onClick={() => {
                    setEditId(d.id);
                    setForm({
                      nombre: d.nombre,
                      descripcion: d.descripcion || "",
                    });
                    setError("");
                  }}
                >
                  Editar
                </button>{" "}
                <button onClick={() => eliminar(d.id)} style={{ color: "red" }}>
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
