from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.blood_request import RequestStatus
from ..models.user import Role, User
from ..schemas.blood_request import (
    BloodRequestCreate,
    BloodRequestResponse,
    BloodRequestStatusUpdate,
)
from ..services import blood_request as service
from ..services import doctor as doctor_service

router = APIRouter(prefix="/blood-requests", tags=["Blood Requests"])

VIEW_ALL_ROLES = (Role.admin, Role.staff, Role.doctor)


@router.post(
    "/",
    response_model=BloodRequestResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.doctor))],
)
def create_blood_request(
    data: BloodRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doctor_profile = doctor_service.get_by_user_id(db, current_user.id)
    if not doctor_profile:
        raise HTTPException(
            status_code=400,
            detail="Your account has no linked doctor profile, so it cannot create a request",
        )
    return service.create(db, data, requested_by_id=doctor_profile.id)


@router.get(
    "/",
    response_model=list[BloodRequestResponse],
    dependencies=[Depends(require_roles(*VIEW_ALL_ROLES))],
)
def list_blood_requests(
    skip: int = 0,
    limit: int = 100,
    patient_id: int | None = None,
    status: RequestStatus | None = None,
    db: Session = Depends(get_db),
):
    return service.get_all(db, skip, limit, patient_id, status)


@router.get(
    "/{request_id}",
    response_model=BloodRequestResponse,
    dependencies=[Depends(require_roles(*VIEW_ALL_ROLES))],
)
def get_blood_request(request_id: int, db: Session = Depends(get_db)):
    req = service.get_by_id(db, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Blood request not found")
    return req


@router.put(
    "/{request_id}/status",
    response_model=BloodRequestResponse,
    dependencies=[Depends(require_roles(Role.admin, Role.staff))],
)
def update_blood_request_status(
    request_id: int, data: BloodRequestStatusUpdate, db: Session = Depends(get_db)
):
    req = service.get_by_id(db, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Blood request not found")
    return service.update_status(db, req, data.status)