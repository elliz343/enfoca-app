# Enfoca — Organizador de tareas para estudiantes

## Cómo correrlo

1. Instala las dependencias:
   pip install -r requirements.txt

2. Corre el servidor:
   python main.py

3. Abre en el navegador:
   http://12c7.0.0.1:5000

## Estructura

- main.py              -> rutas de la app (front y API)
- backend/database.py   -> conexión a SQLite (patrón Singleton)
- backend/models.py     -> clases Usuario y Tarea
- backend/repositories.py -> acceso a datos (patrón Repository)
- backend/services.py   -> lógica de negocio (validaciones, reglas)
- templates/            -> las 4 páginas (home, login, registro, dashboard)
- static/css/style.css  -> estilos (azul y verde, patrón F, diseño en cajas)

La base de datos (enfoca.db) se crea sola la primera vez que corres main.py.
