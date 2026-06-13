import { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { Login } from "./pages/Login";
import { Estudiantes } from "./pages/Estudiantes";
import { Actividades } from "./pages/Actividades";
import { Disciplinas } from "./pages/Disciplinas";
import { Espacios } from "./pages/Espacios";
import { Inscripciones } from "./pages/Inscripciones";
import { Asistencias } from "./pages/Asistencias";
import { Reportes } from "./pages/Reportes";
import "./App.css";

function App() {
  const [rol, setRol] = useState(null);

  if (!rol) return <Login onLogin={setRol} />;

  return (
    <BrowserRouter>
      <Navbar rol={rol} onLogout={() => setRol(null)} />
      <div style={{ padding: "20px" }}>
        <Routes>
          {rol === "ADMIN" && (
            <>
              <Route path="/estudiantes" element={<Estudiantes rol={rol} />} />
              <Route path="/disciplinas" element={<Disciplinas rol={rol} />} />
              <Route path="/espacios" element={<Espacios rol={rol} />} />
              <Route path="/actividades" element={<Actividades rol={rol} />} />
              <Route
                path="/inscripciones"
                element={<Inscripciones rol={rol} />}
              />
              <Route path="/asistencias" element={<Asistencias rol={rol} />} />
              <Route path="/reportes" element={<Reportes rol={rol} />} />
              <Route path="*" element={<Navigate to="/estudiantes" />} />
            </>
          )}
          {rol === "DOCENTE" && (
            <>
              <Route path="/actividades" element={<Actividades rol={rol} />} />
              <Route
                path="/inscripciones"
                element={<Inscripciones rol={rol} />}
              />
              <Route path="/asistencias" element={<Asistencias rol={rol} />} />
              <Route path="/reportes" element={<Reportes rol={rol} />} />
              <Route path="*" element={<Navigate to="/actividades" />} />
            </>
          )}
          {rol === "ESTUDIANTE" && (
            <>
              <Route path="/actividades" element={<Actividades rol={rol} />} />
              <Route
                path="/inscripciones"
                element={<Inscripciones rol={rol} />}
              />
              <Route path="*" element={<Navigate to="/actividades" />} />
            </>
          )}
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
