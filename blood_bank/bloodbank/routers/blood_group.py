from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.user import Role, User
from ..schemas.blood_group import (
    BloodGroupCreate,
    BloodGroupResponse,
    BloodGroupUpdate,
)
from ..services import blood_group as service


router = APIRouter(prefix="/blood-groups", tags=["Blood Groups"])


@router.post("/", response_model=BloodGroupResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(Role.admin))],)
def create_blood_group(data: BloodGroupCreate, db: Session = Depends(get_db)):
    if service.get_by_name(db, data.name):
        raise HTTPException(status_code=409, detail="Blood group already exists")
    return service.create(db, data)


@router.get("/", response_model=list[BloodGroupResponse])
def list_blood_groups(
    skip: int = 0,
    limit: int = 100,
    q: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_all(db, skip=skip, limit=limit, q=q)


@router.get("/{blood_group_id}", response_model=BloodGroupResponse)
def get_blood_group(blood_group_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user),):
    blood_group = service.get_by_id(db, blood_group_id)
    if not blood_group:
        raise HTTPException(status_code=404, detail="Blood group not found")
    return blood_group


@router.put("/{blood_group_id}", response_model=BloodGroupResponse, dependencies=[Depends(require_roles(Role.admin))],)
def update_blood_group(
    blood_group_id: int, data: BloodGroupUpdate, db: Session = Depends(get_db)
):
    blood_group = service.get_by_id(db, blood_group_id)
    if not blood_group:
        raise HTTPException(status_code=404, detail="Blood group not found")
    existing = service.get_by_name(db, data.name)
    if existing and existing.id != blood_group_id:
        raise HTTPException(status_code=409, detail="Blood group already exists")
    return service.update(db, blood_group, data)


@router.delete("/{blood_group_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(Role.admin))],)
def delete_blood_group(blood_group_id: int, db: Session = Depends(get_db)):
    blood_group = service.get_by_id(db, blood_group_id)
    if not blood_group:
        raise HTTPException(status_code=404, detail="Blood group not found")
    service.delete(db, blood_group)