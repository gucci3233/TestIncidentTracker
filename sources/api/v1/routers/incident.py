from fastapi import Depends, Query
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession

from sources.database import session
from sources.models import Incident
from . import router
from ..schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
    IncidentStatus,
)


@router.post("", response_model=IncidentResponse)
async def create_incident(payload: IncidentCreate, db: AsyncSession = Depends(session)):
    inst = await Incident.create(session=db, **payload.model_dump())
    return inst


@router.get("", response_model=list[IncidentResponse])
async def list_incidents(
        status: list[IncidentStatus] = Query(default=[IncidentStatus.new], description="Filter by statuses"),
        db: AsyncSession = Depends(session),
):
    filters: dict = {}
    if status:
        filters["status__in"] = [s.value for s in status]

    results = await Incident.get_all(session=db, order_by=(desc(Incident.created_at),), **filters)
    return results


@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(
        incident_id: int, db: AsyncSession = Depends(session)
):
    result = await Incident.get_or_404(session=db, id=incident_id)
    return result


@router.patch("/{incident_id}", response_model=IncidentResponse)
async def patch_incident(
        incident_id: int, payload: IncidentUpdate, db: AsyncSession = Depends(session)
):
    obj = await Incident.get_or_404(session=db, id=incident_id)
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    await obj.update(session=db)
    return obj


@router.delete("/{incident_id}", response_model=None)
async def delete_incident(
        incident_id: int, db: AsyncSession = Depends(session)
):
    obj = await Incident.get_or_404(session=db, id=incident_id)
    await obj.delete(session=db)
    return {"detail": "Deleted Successfully."}
