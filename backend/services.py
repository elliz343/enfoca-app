"""
Capa de servicios: contiene la lógica de negocio (validaciones,
reglas de la app). Las rutas (main.py) solo reciben la petición HTTP
y llaman a estos servicios; no saben nada de SQL (separación de capas).
"""
from werkzeug.security import generate_password_hash, check_password_hash
from .repositories import UsuarioRepository, TareaRepository
from .models import Usuario, Tarea


class AuthService:
    def __init__(self, usuario_repo: UsuarioRepository = None):
        # Inyección de dependencias: si no se pasa un repo, usa el real.
        # Facilita probar el servicio con un repositorio falso (mock).
        self.usuario_repo = usuario_repo or UsuarioRepository()

    def registrar(self, nombre: str, email: str, password: str) -> Usuario:
        if not nombre or not email or not password:
            raise ValueError("Todos los campos son obligatorios")
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        if self.usuario_repo.obtener_por_email(email):
            raise ValueError("Ese correo ya está registrado")
        usuario = Usuario(
            id=None,
            nombre=nombre,
            email=email,
            password_hash=generate_password_hash(password),
        )
        return self.usuario_repo.crear(usuario)

    def iniciar_sesion(self, email: str, password: str) -> Usuario:
        usuario = self.usuario_repo.obtener_por_email(email)
        if not usuario or not check_password_hash(usuario.password_hash, password):
            raise ValueError("Correo o contraseña incorrectos")
        return usuario


class TareaService:
    def __init__(self, tarea_repo: TareaRepository = None):
        self.tarea_repo = tarea_repo or TareaRepository()

    def crear_tarea(self, usuario_id: int, titulo: str, materia: str, fecha: str) -> Tarea:
        if not titulo:
            raise ValueError("La tarea necesita un título")
        tarea = Tarea(id=None, usuario_id=usuario_id, titulo=titulo, materia=materia, fecha=fecha)
        return self.tarea_repo.crear(tarea)

    def listar_tareas(self, usuario_id: int):
        return self.tarea_repo.listar_por_usuario(usuario_id)

    def eliminar_tarea(self, tarea_id: int, usuario_id: int) -> None:
        self.tarea_repo.eliminar(tarea_id, usuario_id)
