from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.user import Role, User
from ..schemas.patient import (
    PatientAdminUpdate,
    PatientCreate,
    PatientDoctorUpdate,
    PatientPublicView,
    PatientResponse,
    PatientSelfUpdate,
)
from ..services import patient as service

router = APIRouter(prefix="/patients", tags=["Patients"])

FULL_VIEW_ROLES = (Role.admin, Role.staff, Role.doctor)


@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.admin, Role.staff))],
)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get(
    "/",
    response_model=list[PatientResponse],
    dependencies=[Depends(require_roles(*FULL_VIEW_ROLES))],
)
def list_patients(
    skip: int = 0, limit: int = 100, q: str | None = None, db: Session = Depends(get_db)
):
    return service.get_all(db, skip, limit, q)


@router.get("/me", response_model=PatientResponse)
def get_my_patient_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = service.get_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=404, detail="No patient profile linked to your account")
    return patient


@router.put("/me", response_model=PatientResponse)
def update_my_patient_profile(
    data: PatientSelfUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != Role.patient:
        raise HTTPException(status_code=403, detail="Only patients can update their own profile")
    patient = service.get_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=404, detail="No patient profile linked to your account")
    return service.update(db, patient, data)


@router.get("/{patient_id}")
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = service.get_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    is_owner = patient.user_id == current_user.id
    if current_user.role in FULL_VIEW_ROLES or is_owner:
        return PatientResponse.model_validate(patient)
    if current_user.role == Role.donor:
        return PatientPublicView.model_validate(patient)
    raise HTTPException(status_code=403, detail="Not allowed to view this patient")


@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
    dependencies=[Depends(require_roles(Role.admin, Role.staff))],
)
def update_patient(patient_id: int, data: PatientAdminUpdate, db: Session = Depends(get_db)):
    patient = service.get_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return service.update(db, patient, data)


@router.put(
    "/{patient_id}/medical",
    response_model=PatientResponse,
    dependencies=[Depends(require_roles(Role.doctor))],
)
def update_patient_medical(
    patient_id: int, data: PatientDoctorUpdate, db: Session = Depends(get_db)
):
    patient = service.get_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return service.update(db, patient, data)


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(Role.admin))],
)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = service.get_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    service.delete(db, patient)