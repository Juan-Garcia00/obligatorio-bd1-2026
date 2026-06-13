import { Link } from "react-router-dom";

export const Navbar = ({ rol, onLogout }) => {
  const linksAdmin = [
    { to: "/estudiantes", label: "Estudiantes" },
    { to: "/disciplinas", label: "Disciplinas" },
    { to: "/espacios", label: "Espacios" },
    { to: "/actividades", label: "Actividades" },
    { to: "/inscripciones", label: "Inscripciones" },
    { to: "/asistencias", label: "Asistencias" },
    { to: "/reportes", label: "Reportes" },
  ];
  const linksDocente = [
    { to: "/actividades", label: "Actividades" },
    { to: "/inscripciones", label: "Inscripciones" },
    { to: "/asistencias", label: "Asistencias" },
    { to: "/reportes", label: "Reportes" },
  ];
  const linksEstudiante = [
    { to: "/actividades", label: "Actividades" },
    { to: "/inscripciones", label: "Mis Inscripciones" },
  ];

  const links =
    rol === "ADMIN"
      ? linksAdmin
      : rol === "DOCENTE"
        ? linksDocente
        : linksEstudiante;

  return (
    <nav
      style={{
        background: "#1a1a2e",
        padding: "12px 20px",
        display: "flex",
        alignItems: "center",
        gap: "16px",
        flexWrap: "wrap",
      }}
    >
      <span style={{ color: "#fff", fontWeight: "bold", marginRight: "8px" }}>
        🏋️ Deportes
      </span>
      {links.map((l) => (
        <Link
          key={l.to}
          to={l.to}
          style={{ color: "#a0c4ff", textDecoration: "none", fontSize: "14px" }}
        >
          {l.label}
        </Link>
      ))}
      <span style={{ marginLeft: "auto", color: "#ccc", fontSize: "13px" }}>
        Rol: <strong style={{ color: "#fff" }}>{rol}</strong>
      </span>
      <button
        onClick={onLogout}
        style={{
          background: "#e63946",
          color: "#fff",
          border: "none",
          padding: "6px 12px",
          cursor: "pointer",
          borderRadius: "4px",
          fontSize: "13px",
        }}
      >
        Cerrar sesión
      </button>
    </nav>
  );
};
