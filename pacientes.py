from fastapi import APIRouter, HTTPException, Query
from models import Paciente, PacienteCreate
from storage import CsvRepo

repo = CsvRepo("pacientes.csv", Paciente)
router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("", response_model=Paciente, status_code=201)
def crear_paciente(data: PacienteCreate):
    if any(p.documento == data.documento for p in repo.all()):
        raise HTTPException(409, "Ya existe un paciente con ese documento")
    return repo.add(data.model_dump())


@router.get("", response_model=list[Paciente])
def listar_pacientes(
    nombre: str | None = Query(None, description="Buscar por parte del nombre"),
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Máximo de registros"),
):
    pacientes = repo.all()
    if nombre:
        pacientes = [p for p in pacientes if nombre.lower() in p.nombre.lower()]
    return pacientes[skip : skip + limit]


@router.get("/{paciente_id}", response_model=Paciente)
def obtener_paciente(paciente_id: int):
    paciente = repo.get(paciente_id)
    if not paciente:
        raise HTTPException(404, "Paciente no encontrado")
    return paciente


@router.put("/{paciente_id}", response_model=Paciente)
def actualizar_paciente(paciente_id: int, data: PacienteCreate):
    paciente = repo.update(paciente_id, data.model_dump())
    if not paciente:
        raise HTTPException(404, "Paciente no encontrado")
    return paciente


@router.delete("/{paciente_id}", status_code=204)
def eliminar_paciente(paciente_id: int):
    if not repo.delete(paciente_id):
        raise HTTPException(404, "Paciente no encontrado")
