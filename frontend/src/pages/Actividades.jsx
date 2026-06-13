import { useEffect, useState } from "react";

const API = "http://localhost:5000";
const DIAS = [
  "LUNES",
  "MARTES",
  "MIERCOLES",
  "JUEVES",
  "VIERNES",
  "SABADO",
  "DOMINGO",
];
const ESTADOS = ["ABIERTA", "CERRADA", "FINALIZADA", "CANCELADA"];

export const Actividades = ({ rol }) => {
  const [actividades, setActividades] = useState([]);
  const [disciplinas, setDisciplinas] = useState([]);
  const [espacios, setEspacios] = useState([]);
  const [form, setForm] = useState({
    nombre: "",
    disciplina_id: "",
    espacio_id: "",
    cupo_maximo: "",
    dia_semana: "",
    hora_inicio: "",
    hora_fin: "",
    estado: "ABIERTA",
  });
  const [editId, setEditId] = useState(null);
  const [error, setError] = useState("");

  const headers = { "Content-Type": "application/json", "X-Rol": rol };

  const cargar = () => {
    fetch(`${API}/actividades`, { headers })
      .then((r) => r.json())
      .then(setActividades);
    if (rol === "ADMIN") {
      fetch(`${API}/disciplinas`, { headers })
        .then((r) => r.json())
        .then(setDisciplinas);
      fetch(`${API}/espacios`, { headers })
        .then((r) => r.json())
        .then(setEspacios);
    }
  };

  useEffect(() => {
    cargar();
  }, []);

  const limpiar = () => {
    setForm({
      nombre: "",
      disciplina_id: "",
      espacio_id: "",
      cupo_maximo: "",
      dia_semana: "",
      hora_inicio: "",
      hora_fin: "",
      estado: "ABIERTA",
    });
    setEditId(null);
    setError("");
  };

  const guardar = () => {
    if (
      !form.nombre ||
      !form.disciplina_id ||
      !form.espacio_id ||
      !form.cupo_maximo ||
      !form.dia_semana ||
      !form.hora_inicio ||
      !form.hora_fin
    ) {
      setError("Todos los campos son obligatorios");
      return;
    }
    const url = editId ? `${API}/actividades/${editId}` : `${API}/actividades`;
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

  const editar = (a) => {
    setEditId(a.id);
    setForm({
      nombre: a.nombre,
      disciplina_id: a.disciplina_id,
      espacio_id: a.espacio_id,
      cupo_maximo: a.cupo_maximo,
      dia_semana: a.dia_semana,
      hora_inicio: a.hora_inicio,
      hora_fin: a.hora_fin,
      estado: a.estado,
    });
    setError("");
  };

  const eliminar = (id) => {
    if (!confirm("¿Eliminar actividad?")) return;
    fetch(`${API}/actividades/${id}`, { method: "DELETE", headers })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          return;
        }
        cargar();
      });
  };

  const inscribirse = (actividad_id) => {
    const estudiante_id = prompt("Ingresá tu ID de estudiante:");
    if (!estudiante_id) return;
    fetch(`${API}/inscripciones`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        estudiante_id: parseInt(estudiante_id),
        actividad_id,
      }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          return;
        }
        alert(
          `Inscripción ${data.estado === "CONFIRMADA" ? "confirmada ✅" : "en lista de espera ⏳"}`,
        );
      });
  };

  return (
    <div>
      <h2>Actividades deportivas</h2>

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
            {editId ? "Editar actividad" : "Nueva actividad"}
          </h3>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <input
              placeholder="Nombre"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            />
            <select
              value={form.disciplina_id}
              onChange={(e) =>
                setForm({ ...form, disciplina_id: e.target.value })
              }
            >
              <option value="">-- Disciplina --</option>
              {disciplinas.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.nombre}
                </option>
              ))}
            </select>
            <select
              value={form.espacio_id}
              onChange={(e) => setForm({ ...form, espacio_id: e.target.value })}
            >
              <option value="">-- Espacio --</option>
              {espacios.map((e) => (
                <option key={e.id} value={e.id}>
                  {e.nombre}
                </option>
              ))}
            </select>
            <input
              placeholder="Cupo máximo"
              type="number"
              value={form.cupo_maximo}
              onChange={(e) =>
                setForm({ ...form, cupo_maximo: e.target.value })
              }
            />
            <select
              value={form.dia_semana}
              onChange={(e) => setForm({ ...form, dia_semana: e.target.value })}
            >
              <option value="">-- Día --</option>
              {DIAS.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
            <input
              placeholder="Hora inicio (HH:MM)"
              value={form.hora_inicio}
              onChange={(e) =>
                setForm({ ...form, hora_inicio: e.target.value })
              }
            />
            <input
              placeholder="Hora fin (HH:MM)"
              value={form.hora_fin}
              onChange={(e) => setForm({ ...form, hora_fin: e.target.value })}
            />
            <select
              value={form.estado}
              onChange={(e) => setForm({ ...form, estado: e.target.value })}
            >
              {ESTADOS.map((s) => (
                <option key={s} value={s}>
                  {s}
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
            <th>Nombre</th>
            <th>Disciplina</th>
            <th>Espacio</th>
            <th>Día</th>
            <th>Inicio</th>
            <th>Fin</th>
            <th>Cupo</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {actividades.map((a) => (
            <tr key={a.id}>
              <td>{a.nombre}</td>
              <td>{a.disciplina_nombre}</td>
              <td>{a.espacio_nombre}</td>
              <td>{a.dia_semana}</td>
              <td>{a.hora_inicio}</td>
              <td>{a.hora_fin}</td>
              <td>{a.cupo_maximo}</td>
              <td>{a.estado}</td>
              <td>
                {rol === "ADMIN" && (
                  <>
                    <button onClick={() => editar(a)}>Editar</button>{" "}
                    <button
                      onClick={() => eliminar(a.id)}
                      style={{ color: "red" }}
                    >
                      Eliminar
                    </button>
                  </>
                )}
                {rol === "ESTUDIANTE" && a.estado === "ABIERTA" && (
                  <button onClick={() => inscribirse(a.id)}>Inscribirse</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
