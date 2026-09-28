from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.user import Role, User
from ..schemas.donor import (
    DonorAdminUpdate,
    DonorCreate,
    DonorResponse,
    DonorSelfUpdate,
)
from ..services import donor as service

router = APIRouter(prefix="/donors", tags=["Donors"])

STAFF_VIEW_ROLES = (Role.admin, Role.staff, Role.doctor)


@router.post(
    "/",
    response_model=DonorResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.admin, Role.staff))],
)
def create_donor(data: DonorCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get(
    "/",
    response_model=list[DonorResponse],
    dependencies=[Depends(require_roles(*STAFF_VIEW_ROLES))],
)
def list_donors(
    skip: int = 0,
    limit: int = 100,
    q: str | None = None,
    blood_group_id: int | None = None,
    db: Session = Depends(get_db),
):
    return service.get_all(db, skip, limit, q, blood_group_id)


# --- specific paths BEFORE the dynamic {donor_id} path ---

@router.get("/me", response_model=DonorResponse)
def get_my_donor_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    donor = service.get_by_user_id(db, current_user.id)
    if not donor:
        raise HTTPException(status_code=404, detail="No donor profile linked to your account")
    return donor


@router.put("/me", response_model=DonorResponse)
def update_my_donor_profile(
    data: DonorSelfUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != Role.donor:
        raise HTTPException(status_code=403, detail="Only donors can update their own profile")
    donor = service.get_by_user_id(db, current_user.id)
    if not donor:
        raise HTTPException(status_code=404, detail="No donor profile linked to your account")
    return service.update(db, donor, data)


@router.get("/{donor_id}", response_model=DonorResponse)
def get_donor(
    donor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    donor = service.get_by_id(db, donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    is_owner = donor.user_id == current_user.id
    if current_user.role not in STAFF_VIEW_ROLES and not is_owner:
        raise HTTPException(status_code=403, detail="Not allowed to view this donor")
    return donor


@router.put(
    "/{donor_id}",
    response_model=DonorResponse,
    dependencies=[Depends(require_roles(Role.admin, Role.staff))],
)
def update_donor(donor_id: int, data: DonorAdminUpdate, db: Session = Depends(get_db)):
    donor = service.get_by_id(db, donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return service.update(db, donor, data)


@router.delete(
    "/{donor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(Role.admin))],
)
def delete_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = service.get_by_id(db, donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    service.delete(db, donor)