import { useEffect, useState } from "react";

export const Estudiantes = ({ rol }) => {
  const [estudiantes, setEstudiantes] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/estudiantes", {
      headers: { "X-Rol": rol },
    })
      .then((res) => res.json())
      .then((data) => setEstudiantes(data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Estudiantes</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Documento</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {estudiantes.map((e) => (
            <tr key={e.id}>
              <td>{e.documento}</td>
              <td>{e.nombre}</td>
              <td>{e.apellido}</td>
              <td>{e.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
