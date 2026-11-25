# Enfoca — Organizador de tareas para estudiantes

## Cómo correrlo

1.SET LOCATION ENFOCA-APP-FOLDER.

2. Instala las dependencias:
   pip install -r requirements.txt
   
4. Copiar en PowerShell
   
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USERNAME = "thomassantiagodamian@gmail.com"     - PRESS ENTER.
$env:SMTP_FROM = "thomassantiagodamian@gmail.com"         - PRESS ENTER.

Luego de eso, copiar:     $secure = Read-Host -Prompt "Contraseña de aplicación" -AsSecureString       - PRESS ENTER

LUEGO DEBEMOS COPIAR LA CONTRASEÑA COMO SE INDICA;      -PRESS ENTER

POR ULTIMO COPIAR:    $env:SMTP_PASSWORD = [System.Net.NetworkCredential]::new("", $secure).Password   - PRESS ENTER - DE ESTA MANERA SE HABILITAN LOS CORREOS.

   
3. Corre el servidor:
   py main.py 

4. Abre en el navegador:
   http://12c7.0.0.1:5000

## Estructura

- main.py              -> rutas de la app (front y API)
- backend/database.py   -> conexión a SQLite (patrón Singleton)
- backend/models.py     -> clases Usuario y Tarea
- backend/repositories.py -> acceso a datos (patrón Repository)
- backend/services.py   -> lógica de negocio (validaciones, reglas)
- templates/            -> las 4 páginas (home, login, registro, dashboard)
- static/css/style.css  -> estilos (azul y verde, patrón F, diseño en cajas)
- backend/email_service.py` -> envío de correos mediante SMTP.
La base de datos (enfoca.db) se crea sola la primera vez que corres main.py.
