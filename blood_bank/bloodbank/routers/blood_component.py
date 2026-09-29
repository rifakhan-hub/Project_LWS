from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.user import Role
from ..schemas.blood_component import (
    BloodComponentCreate,
    BloodComponentResponse,
    BloodComponentUpdate,
)
from ..services import blood_component as service

router = APIRouter(prefix="/blood-components", tags=["Blood Components"])


@router.post(
    "/",
    response_model=BloodComponentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.admin))],
)
def create_blood_component(data: BloodComponentCreate, db: Session = Depends(get_db)):
    if service.get_by_name(db, data.name):
        raise HTTPException(status_code=409, detail="Blood component already exists")
    return service.create(db, data)


@router.get(
    "/",
    response_model=list[BloodComponentResponse],
    dependencies=[Depends(get_current_user)],
)
def list_blood_components(
    skip: int = 0, limit: int = 100, q: str | None = None, db: Session = Depends(get_db)
):
    return service.get_all(db, skip, limit, q)


@router.get(
    "/{component_id}",
    response_model=BloodComponentResponse,
    dependencies=[Depends(get_current_user)],
)
def get_blood_component(component_id: int, db: Session = Depends(get_db)):
    component = service.get_by_id(db, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Blood component not found")
    return component


@router.put(
    "/{component_id}",
    response_model=BloodComponentResponse,
    dependencies=[Depends(require_roles(Role.admin))],
)
def update_blood_component(
    component_id: int, data: BloodComponentUpdate, db: Session = Depends(get_db)
):
    component = service.get_by_id(db, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Blood component not found")
    existing = service.get_by_name(db, data.name)
    if existing and existing.id != component_id:
        raise HTTPException(status_code=409, detail="Blood component already exists")
    return service.update(db, component, data)


@router.delete(
    "/{component_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(Role.admin))],
)
def delete_blood_component(component_id: int, db: Session = Depends(get_db)):
    component = service.get_by_id(db, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Blood component not found")
    service.delete(db, component)