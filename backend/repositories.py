"""
Patrón Repository: aísla el acceso a datos (SQL) del resto de la app.
Los Services dependen de estas clases, no de sqlite3 directamente
(principio de inversión de dependencias).
Cada repositorio tiene una sola responsabilidad: una tabla.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from .database import Database
from .models import Usuario, Tarea


class BaseRepository(ABC):
    """Contrato que cualquier repositorio debe cumplir."""
    @abstractmethod
    def obtener_por_id(self, id_: int):
        ...


class UsuarioRepository(BaseRepository):
    def __init__(self):
        self.conexion = Database().obtener_conexion()

    def crear(self, usuario: Usuario) -> Usuario:
        cur = self.conexion.cursor()
        cur.execute(
            "INSERT INTO usuarios (nombre, email, password_hash) VALUES (?, ?, ?)",
            (usuario.nombre, usuario.email, usuario.password_hash),
        )
        self.conexion.commit()
        usuario.id = cur.lastrowid
        return usuario

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        cur = self.conexion.cursor()
        fila = cur.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()
        return self._fila_a_usuario(fila) if fila else None

    def obtener_por_id(self, id_: int) -> Optional[Usuario]:
        cur = self.conexion.cursor()
        fila = cur.execute(
            "SELECT * FROM usuarios WHERE id = ?", (id_,)
        ).fetchone()
        return self._fila_a_usuario(fila) if fila else None

    @staticmethod
    def _fila_a_usuario(fila) -> Usuario:
        return Usuario(
            id=fila["id"],
            nombre=fila["nombre"],
            email=fila["email"],
            password_hash=fila["password_hash"],
        )


class TareaRepository(BaseRepository):
    def __init__(self):
        self.conexion = Database().obtener_conexion()

    def crear(self, tarea: Tarea) -> Tarea:
        cur = self.conexion.cursor()
        cur.execute(
            "INSERT INTO tareas (usuario_id, titulo, materia, fecha) VALUES (?, ?, ?, ?)",
            (tarea.usuario_id, tarea.titulo, tarea.materia, tarea.fecha),
        )
        self.conexion.commit()
        tarea.id = cur.lastrowid
        return tarea

    def listar_por_usuario(self, usuario_id: int) -> List[Tarea]:
        cur = self.conexion.cursor()
        filas = cur.execute(
            "SELECT * FROM tareas WHERE usuario_id = ? ORDER BY fecha IS NULL, fecha ASC",
            (usuario_id,),
        ).fetchall()
        return [self._fila_a_tarea(f) for f in filas]

    def eliminar(self, id_: int, usuario_id: int) -> None:
        cur = self.conexion.cursor()
        cur.execute(
            "DELETE FROM tareas WHERE id = ? AND usuario_id = ?", (id_, usuario_id)
        )
        self.conexion.commit()

    def obtener_por_id(self, id_: int) -> Optional[Tarea]:
        cur = self.conexion.cursor()
        fila = cur.execute("SELECT * FROM tareas WHERE id = ?", (id_,)).fetchone()
        return self._fila_a_tarea(fila) if fila else None

    @staticmethod
    def _fila_a_tarea(fila) -> Tarea:
        return Tarea(
            id=fila["id"],
            usuario_id=fila["usuario_id"],
            titulo=fila["titulo"],
            materia=fila["materia"],
            fecha=fila["fecha"],
        )
