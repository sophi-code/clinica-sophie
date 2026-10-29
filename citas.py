from datetime import date
from fastapi import APIRouter, HTTPException, Query
from models import Cita, CitaCreate, EstadoCita
import medicos
import pacientes
from storage import CsvRepo

repo = CsvRepo("citas.csv", Cita)
router = APIRouter(prefix="/citas", tags=["Citas"])


def hay_cruce(
    medico_id: int, fecha_hora, ignorar_id: int | None = None
) -> bool:
    """Regla de negocio: un médico no puede tener 2 citas a la misma hora."""
    return any(
        c.medico_id == medico_id
        and c.fecha_hora == fecha_hora
        and c.estado != EstadoCita.CANCELADA
        and c.id != ignorar_id
        for c in repo.all()
    )


def validar(data: CitaCreate, ignorar_id: int | None = None):
    if not pacientes.repo.get(data.paciente_id):
        raise HTTPException(404, "El paciente no existe")
    if not medicos.repo.get(data.medico_id):
        raise HTTPException(404, "El médico no existe")
    if hay_cruce(data.medico_id, data.fecha_hora, ignorar_id):
        raise HTTPException(409, "El médico ya tiene una cita en ese horario")


@router.post("", response_model=Cita, status_code=201)
def agendar_cita(data: CitaCreate):
    validar(data)
    return repo.add(data.model_dump())


@router.get("", response_model=list[Cita])
def listar_citas(
    paciente_id: int | None = Query(None, description="Filtrar por paciente"),
    medico_id: int | None = Query(None, description="Filtrar por médico"),
    estado: EstadoCita
    | None = Query(None, description="Filtrar por estado"),
    fecha: date | None = Query(None, description="Filtrar por día (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    citas = repo.all()
    if paciente_id:
        citas = [c for c in citas if c.paciente_id == paciente_id]
    if medico_id:
        citas = [c for c in citas if c.medico_id == medico_id]
    if estado:
        citas = [c for c in citas if c.estado == estado]
    if fecha:
        citas = [c for c in citas if c.fecha_hora.date() == fecha]
    return citas[skip : skip + limit]


@router.get("/{cita_id}", response_model=Cita)
def obtener_cita(cita_id: int):
    cita = repo.get(cita_id)
    if not cita:
        raise HTTPException(404, "Cita no encontrada")
    return cita


@router.put("/{cita_id}", response_model=Cita)
def reprogramar_cita(cita_id: int, data: CitaCreate):
    if not repo.get(cita_id):
        raise HTTPException(404, "Cita no encontrada")
    validar(data, ignorar_id=cita_id)
    return repo.update(cita_id, data.model_dump())


@router.delete("/{cita_id}", status_code=204)
def eliminar_cita(cita_id: int):
    if not repo.delete(cita_id):
        raise HTTPException(404, "Cita no encontrada")


# ---------- Cambios de estado (diagrama de estados) ----------
def cambiar_estado(cita_id: int, permitidos: set, nuevo: EstadoCita):
    cita = repo.get(cita_id)
    if not cita:
        raise HTTPException(404, "Cita no encontrada")
    if cita.estado not in permitidos:
        raise HTTPException(
            409, f"No se puede pasar de {cita.estado.value} a {nuevo.value}"
        )
    return repo.update(cita_id, {"estado": nuevo})


@router.patch("/{cita_id}/confirmar", response_model=Cita)
def confirmar_cita(cita_id: int):
    return cambiar_estado(
        cita_id, {EstadoCita.PENDIENTE}, EstadoCita.CONFIRMADA
    )


@router.patch("/{cita_id}/atender", response_model=Cita)
def atender_cita(cita_id: int):
    return cambiar_estado(
        cita_id, {EstadoCita.CONFIRMADA}, EstadoCita.ATENDIDA
    )


@router.patch("/{cita_id}/cancelar", response_model=Cita)
def cancelar_cita(cita_id: int):
    return cambiar_estado(
        cita_id,
        {EstadoCita.PENDIENTE, EstadoCita.CONFIRMADA},
        EstadoCita.CANCELADA,
    )
