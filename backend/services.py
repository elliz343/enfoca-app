"""
Capa de servicios: contiene la lógica de negocio (validaciones,
reglas de la app). Las rutas (main.py) solo reciben la petición HTTP
y llaman a estos servicios; no saben nada de SQL (separación de capas).
"""
from datetime import date, datetime, timedelta, timezone
import hashlib
import secrets

from werkzeug.security import generate_password_hash, check_password_hash

from .repositories import UsuarioRepository, TareaRepository
from .models import Usuario, Tarea


class AuthService:
    def __init__(self, usuario_repo: UsuarioRepository = None):
        self.usuario_repo = usuario_repo or UsuarioRepository()

    def registrar(self, nombre: str, email: str, password: str) -> Usuario:
        if not nombre or not email or not password:
            raise ValueError("Todos los campos son obligatorios")

        email = email.strip().lower()
        partes = email.split("@")

        if (
            len(partes) != 2
            or not partes[0]
            or not partes[1].endswith(".edu.co")
            or len(partes[1]) <= len(".edu.co")
            or ".." in partes[1]
            or any(caracter.isspace() for caracter in email)
        ):
            raise ValueError("Usa un correo institucional que termine en .edu.co")

        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

        usuario_existente = self.usuario_repo.obtener_por_email(email)

        if usuario_existente:
            if usuario_existente.email_verificado:
                raise ValueError("Ese correo ya está registrado")
        return usuario_existente

        usuario = Usuario(
            id=None,
            nombre=nombre,
            email=email,
            password_hash=generate_password_hash(password),
            email_verificado=False,
        )
        return self.usuario_repo.crear(usuario)

    def crear_token_verificacion(self, email: str) -> str:
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        expira = (
            datetime.now(timezone.utc) + timedelta(hours=24)
        ).isoformat()

        self.usuario_repo.guardar_token_verificacion(
            email, token_hash, expira
        )
        return token

    def verificar_email(self, token: str) -> bool:
        if not token:
            return False

        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        ahora = datetime.now(timezone.utc).isoformat()
        return self.usuario_repo.verificar_email(token_hash, ahora)

    def iniciar_sesion(self, email: str, password: str) -> Usuario:
        email = email.strip().lower()
        usuario = self.usuario_repo.obtener_por_email(email)

        if not usuario or not check_password_hash(usuario.password_hash, password):
            raise ValueError("Correo o contraseña incorrectos")

        if not usuario.email_verificado:
            raise ValueError("Confirma tu correo antes de iniciar sesión")

        return usuario
    

class TareaService:
    def __init__(self, tarea_repo: TareaRepository = None):
        self.tarea_repo = tarea_repo or TareaRepository()

    def crear_tarea(
        self, usuario_id: int, titulo: str, materia: str, fecha: str
    ) -> Tarea:
        if not titulo:
            raise ValueError("La tarea necesita un título")

        fecha = (fecha or "").strip()
        if fecha:
            try:
                fecha_obj = date.fromisoformat(fecha)
            except ValueError as error:
                raise ValueError(
                    "La fecha debe tener el formato AAAA-MM-DD"
                ) from error

            if fecha_obj < date.today():
                raise ValueError("La fecha no puede estar en el pasado")

        tarea = Tarea(
            id=None,
            usuario_id=usuario_id,
            titulo=titulo,
            materia=materia,
            fecha=fecha,
        )
        return self.tarea_repo.crear(tarea)

    def listar_tareas(self, usuario_id: int):
        return self.tarea_repo.listar_por_usuario(usuario_id)

    def eliminar_tarea(self, tarea_id: int, usuario_id: int) -> None:
        self.tarea_repo.eliminar(tarea_id, usuario_id)
