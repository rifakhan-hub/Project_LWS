from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.user import Role
from ..schemas.staff import StaffCreate, StaffResponse, StaffUpdate
from ..services import staff as service

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.post(
    "/",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.admin))],
)
def create_staff(data: StaffCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get(
    "/",
    response_model=list[StaffResponse],
    dependencies=[Depends(get_current_user)],
)
def list_staff(
    skip: int = 0, limit: int = 100, q: str | None = None, db: Session = Depends(get_db)
):
    return service.get_all(db, skip, limit, q)


@router.get(
    "/{staff_id}",
    response_model=StaffResponse,
    dependencies=[Depends(get_current_user)],
)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    staff_member = service.get_by_id(db, staff_id)
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff_member


@router.put(
    "/{staff_id}",
    response_model=StaffResponse,
    dependencies=[Depends(require_roles(Role.admin))],
)
def update_staff(staff_id: int, data: StaffUpdate, db: Session = Depends(get_db)):
    staff_member = service.get_by_id(db, staff_id)
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff not found")
    return service.update(db, staff_member, data)


@router.delete(
    "/{staff_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(Role.admin))],
)
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    staff_member = service.get_by_id(db, staff_id)
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff not found")
    service.delete(db, staff_member)