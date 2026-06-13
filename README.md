# obligatorio-bd1-2026
# Sistema de Gestión de Actividades Deportivas Universitarias

Integrantes:
- Joaquin Bauza
- Joaquin Caceres
- Juan Diego García

Tecnologías:
- MySQL
- Python (Flask)
- React
- Docker

## Instalacion del proyecto

git clone <url-del-repo>
cd obligatorio-bd1-2026

## Cómo correr el proyecto

Requisitos: Docker y Docker Compose instalados.

1. Copiar el ejemplo de abajo a `.env` y completar los valores (o usar los de ejemplo).

MYSQL_ROOT_PASSWORD=changeme
MYSQL_DATABASE=sistema_deportes
DB_HOST=db
DB_USER=root
DB_PASSWORD=changeme
DB_NAME=sistema_deportes

2. `docker-compose up --build`
3. Abrir http://localhost:3000


## ¿Qué es un ABM?

A lo largo de este documento se hace referencia a "ABM", que significa Alta, Baja y Modificación. Un módulo con ABM completo permite crear nuevos registros (Alta), eliminarlos (Baja) y editarlos (Modificación), además de consultarlos.

---

## Inicio de sesión

Al ingresar a la aplicación se muestra una pantalla para seleccionar el rol con el que se va a usar el sistema. No se requiere usuario ni contraseña.

El rol ADMIN tiene acceso completo a todas las funciones del sistema. El rol DOCENTE puede ver actividades e inscripciones, registrar asistencias y consultar reportes. El rol ESTUDIANTE puede ver las actividades disponibles e inscribirse en ellas.

---

## Módulo: Estudiantes *(solo ADMIN)*

**Alta:** se puede registrar un nuevo estudiante completando documento, nombre, apellido, email, carrera y facultad.

**Baja:** se puede eliminar un estudiante de la lista. No se permite eliminar un estudiante que tenga inscripciones asociadas, para no romper el historial de inscripciones y asistencias.

**Modificación:** se pueden editar los datos de un estudiante ya registrado (documento, nombre, apellido, email, carrera, facultad).

**Consulta:** se puede ver el listado completo de estudiantes registrados.

---

## Módulo: Disciplinas *(solo ADMIN)*

**Alta:** se pueden crear nuevas disciplinas deportivas (por ejemplo: fútbol, básquetbol, atletismo, vóleibol, yoga, funcional, gimnasio), indicando nombre y una descripción opcional.

**Baja:** se pueden eliminar disciplinas que ya no se utilicen.

**Modificación:** se puede editar el nombre o la descripción de una disciplina existente.

**Consulta:** se puede ver el listado de disciplinas disponibles.

---

## Módulo: Espacios deportivos *(solo ADMIN)*

**Alta:** se pueden registrar nuevos espacios físicos donde se realizan las actividades, indicando nombre, ubicación y capacidad máxima.

**Baja:** se pueden eliminar espacios. No se permite eliminar un espacio que tenga actividades asociadas.

**Modificación:** se pueden editar el nombre, la ubicación o la capacidad de un espacio existente.

**Consulta:** se puede ver el listado de espacios disponibles.

---

## Módulo: Actividades deportivas

**Alta** *(solo ADMIN)*: se pueden crear nuevas actividades indicando nombre, disciplina, espacio, cupo máximo, día, horario de inicio y fin, y estado.

**Baja** *(solo ADMIN)*: se pueden eliminar actividades existentes.

**Modificación** *(solo ADMIN)*: se pueden editar todos los datos de una actividad, incluyendo su estado.

**Consulta** *(ADMIN, DOCENTE, ESTUDIANTE)*: se puede ver el listado completo de actividades con su disciplina, espacio, horario, cupo y estado.

Los estados posibles de una actividad son: ABIERTA, CERRADA, FINALIZADA y CANCELADA. El ESTUDIANTE solo puede inscribirse en actividades con estado ABIERTA.

---

## Módulo: Inscripciones

**Alta** *(ESTUDIANTE)*: un estudiante puede inscribirse en una actividad con estado ABIERTA. Si la actividad tiene cupo disponible, la inscripción queda en estado CONFIRMADA; si el cupo está completo, la inscripción queda en estado ESPERA. Un estudiante no puede inscribirse dos veces en la misma actividad.

**Baja** *(ADMIN, ESTUDIANTE)*: se puede cancelar una inscripción. Si la inscripción cancelada estaba CONFIRMADA, el primer estudiante que se encuentre en estado ESPERA para esa actividad pasa automáticamente a CONFIRMADA.

**Consulta** *(ADMIN, DOCENTE, ESTUDIANTE)*: se puede ver el listado de inscripciones, incluyendo estudiante, actividad, fecha de inscripción y estado.

---

## Módulo: Asistencias *(ADMIN y DOCENTE)*

**Alta**: se puede registrar la asistencia de un estudiante a una actividad para una fecha determinada, marcando si estuvo presente o ausente. Solo se puede registrar asistencia de estudiantes que tengan una inscripción CONFIRMADA en esa actividad; si el estudiante no está confirmado, el sistema rechaza el registro.

**Consulta**: se puede ver el listado de asistencias registradas, filtrando por actividad si se desea.

---

## Módulo: Reportes *(ADMIN y DOCENTE)*

El sistema permite consultar los siguientes reportes:

- Actividades con más inscriptos confirmados.
- Actividades con cupos disponibles.
- Cantidad de inscriptos por disciplina.
- Cantidad de inscriptos por carrera y facultad.
- Porcentaje de ocupación por actividad.
- Porcentaje de asistencia por actividad.
- Estudiantes con tres o más inasistencias.
- Estudiantes en lista de espera.
- Espacios más utilizados.
- Inscripciones agrupadas por estado.

---

## Reglas de negocio generales

1. Solo se pueden realizar inscripciones en actividades con estado ABIERTA.
2. Si el cupo está lleno, la inscripción queda en estado ESPERA.
3. Un estudiante no puede inscribirse dos veces a la misma actividad.
4. Solo se registra asistencia de estudiantes con inscripción CONFIRMADA.
5. Las actividades CANCELADA o FINALIZADA no aceptan nuevas inscripciones.
6. Al cancelar una inscripción confirmada, se promueve automáticamente al siguiente estudiante en lista de espera.