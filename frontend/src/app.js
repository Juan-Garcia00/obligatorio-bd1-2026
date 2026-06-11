const URL_BACKEND = "http://127.0.0.1:5000";

function cargarActividades() {
  fetch(`${URL_BACKEND}/actividades`)
    .then((response) => response.json())
    .then((data) => {
      const contenedor = document.getElementById("contenedor-actividades");
      contenedor.innerHTML = "";

      if (data.length === 0) {
        contenedor.innerHTML = "<p>No hay actividades creadas.</p>";
        return;
      }

      data.forEach((actividad) => {
        const div = document.createElement("div");
        div.className = "tarjeta";
        div.innerHTML = `
                    <h3>${actividad.nombre}</h3>
                    <p><strong>Disciplina:</strong> ${actividad.disciplina}</p>
                    <p><strong>Lugar:</strong> ${actividad.espacio}</p>
                    <p><strong>Horario:</strong> ${actividad.dia} a las ${actividad.horario}</p>
                    <p><strong>Cupo Máximo:</strong> ${actividad.cupo}</p>
                    <p class="estado">Estado: ${actividad.estado}</p>
                `;
        contenedor.appendChild(div);
      });
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("contenedor-actividades").innerHTML =
        "<p>Error al conectar con el servidor.</p>";
    });
}

window.onload = cargarActividades;
