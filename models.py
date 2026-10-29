from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field


class EstadoCita(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    ATENDIDA = "atendida"
    CANCELADA = "cancelada"


# ---------- Paciente ----------
class PacienteCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    documento: str = Field(min_length=5, max_length=20)
    telefono: str = Field(min_length=7, max_length=15)
    fecha_nacimiento: date


class Paciente(PacienteCreate):
    id: int


# ---------- Médico ----------
class MedicoCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    licencia: str = Field(min_length=3, max_length=20)
    especialidad: str = Field(min_length=3, max_length=50)


class Medico(MedicoCreate):
    id: int


# ---------- Cita ----------
class CitaCreate(BaseModel):
    paciente_id: int = Field(gt=0)
    medico_id: int = Field(gt=0)
    fecha_hora: datetime
    motivo: str = Field(min_length=3, max_length=200)


class Cita(CitaCreate):
    id: int
    estado: EstadoCita = EstadoCita.PENDIENTE
