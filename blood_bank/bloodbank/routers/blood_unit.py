from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.blood_unit import UnitStatus
from ..models.user import Role
from ..schemas.blood_unit import BloodUnitResponse, BloodUnitStatusUpdate
from ..services import blood_unit as service

router = APIRouter(prefix="/blood-units", tags=["Blood Units (Inventory)"])


@router.get(
    "/",
    response_model=list[BloodUnitResponse],
    dependencies=[Depends(get_current_user)],
)
def list_blood_units(
    skip: int = 0,
    limit: int = 100,
    blood_group_id: int | None = None,
    component_id: int | None = None,
    status: UnitStatus | None = None,
    db: Session = Depends(get_db),
):
    return service.get_all(db, skip, limit, blood_group_id, component_id, status)


@router.get(
    "/{unit_id}",
    response_model=BloodUnitResponse,
    dependencies=[Depends(get_current_user)],
)
def get_blood_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = service.get_by_id(db, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Blood unit not found")
    return unit


@router.put(
    "/{unit_id}/status",
    response_model=BloodUnitResponse,
    dependencies=[Depends(require_roles(Role.admin, Role.staff))],
)
def update_blood_unit_status(
    unit_id: int, data: BloodUnitStatusUpdate, db: Session = Depends(get_db)
):
    unit = service.get_by_id(db, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Blood unit not found")
    return service.update_status(db, unit, data.status)