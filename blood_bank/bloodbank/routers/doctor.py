from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.user import Role
from ..schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdate
from ..services import doctor as service

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post(
    "/",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.admin))],
)
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get(
    "/",
    response_model=list[DoctorResponse],
    dependencies=[Depends(get_current_user)],
)
def list_doctors(
    skip: int = 0, limit: int = 100, q: str | None = None, db: Session = Depends(get_db)
):
    return service.get_all(db, skip, limit, q)


@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse,
    dependencies=[Depends(get_current_user)],
)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = service.get_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse,
    dependencies=[Depends(require_roles(Role.admin))],
)
def update_doctor(doctor_id: int, data: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = service.get_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return service.update(db, doctor, data)


@router.delete(
    "/{doctor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(Role.admin))],
)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = service.get_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    service.delete(db, doctor)