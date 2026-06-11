const URL_BACKEND = "http://127.0.0.1:5000";

function cargarActividades() {
  fetch(`${URL_BACKEND}/actividades`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error al obtener actividades");
      }
      return response.json();
    })
    .then((data) => {
      const contenedor = document.getElementById("contenedor-actividades");

      contenedor.innerHTML = "";

      if (data.length === 0) {
        contenedor.innerHTML = "<p>No hay actividades creadas.</p>";
        return;
      }

      data.forEach((actividad) => {
        const tarjeta = document.createElement("div");

        tarjeta.className = "tarjeta";

        tarjeta.innerHTML = `
          <h3>${actividad.nombre}</h3>

          <p>
            <strong>Disciplina:</strong>
            ${actividad.disciplina_nombre}
          </p>

          <p>
            <strong>Espacio:</strong>
            ${actividad.espacio_nombre}
          </p>

          <p>
            <strong>Día:</strong>
            ${actividad.dia_semana}
          </p>

          <p>
            <strong>Horario:</strong>
            ${actividad.hora_inicio} - ${actividad.hora_fin}
          </p>

          <p>
            <strong>Cupo Máximo:</strong>
            ${actividad.cupo_maximo}
          </p>

          <p class="estado">
            Estado: ${actividad.estado}
          </p>
        `;

        contenedor.appendChild(tarjeta);
      });
    })
    .catch((error) => {
      console.error(error);

      document.getElementById("contenedor-actividades").innerHTML = `
        <p>Error al conectar con el servidor.</p>
      `;
    });
}

window.onload = cargarActividades;
