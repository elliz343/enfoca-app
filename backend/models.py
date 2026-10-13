"""
Modelos de dominio: representan los datos, sin lógica de negocio
ni de acceso a datos (principio de responsabilidad única).
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int]
    nombre: str
    email: str
    password_hash: str


@dataclass
class Tarea:
    id: Optional[int]
    usuario_id: int
    titulo: str
    materia: str
    fecha: str
