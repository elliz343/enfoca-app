"""
Patrón Singleton: una sola conexión/punto de acceso a la base de datos
para toda la aplicación, evitando abrir conexiones duplicadas.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "enfoca.db")


class Database:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        self.conexion = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conexion.row_factory = sqlite3.Row
        self._crear_tablas()

    def _crear_tablas(self):
        cur = self.conexion.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                materia TEXT,
                fecha TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        """)
        self.conexion.commit()

    def obtener_conexion(self):
        return self.conexion
