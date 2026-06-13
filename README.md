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
