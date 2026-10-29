from fastapi import APIRouter, HTTPException, Query
from models import Medico, MedicoCreate
from storage import CsvRepo

repo = CsvRepo("medicos.csv", Medico)
router = APIRouter(prefix="/medicos", tags=["Médicos"])


@router.post("", response_model=Medico, status_code=201)
def crear_medico(data: MedicoCreate):
    if any(m.licencia == data.licencia for m in repo.all()):
        raise HTTPException(409, "Ya existe un médico con esa licencia")
    return repo.add(data.model_dump())


@router.get("", response_model=list[Medico])
def listar_medicos(
    especialidad: str
    | None = Query(None, description="Filtrar por especialidad"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    medicos = repo.all()
    if especialidad:
        medicos = [
            m
            for m in medicos
            if especialidad.lower() in m.especialidad.lower()
        ]
    return medicos[skip : skip + limit]


@router.get("/{medico_id}", response_model=Medico)
def obtener_medico(medico_id: int):
    medico = repo.get(medico_id)
    if not medico:
        raise HTTPException(404, "Médico no encontrado")
    return medico


@router.put("/{medico_id}", response_model=Medico)
def actualizar_medico(medico_id: int, data: MedicoCreate):
    medico = repo.update(medico_id, data.model_dump())
    if not medico:
        raise HTTPException(404, "Médico no encontrado")
    return medico


@router.delete("/{medico_id}", status_code=204)
def eliminar_medico(medico_id: int):
    if not repo.delete(medico_id):
        raise HTTPException(404, "Médico no encontrado")
