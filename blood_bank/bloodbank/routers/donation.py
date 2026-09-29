from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.donation import ScreeningStatus
from ..models.user import Role, User
from ..schemas.donation import DonationCreate, DonationResponse, DonationScreeningUpdate
from ..services import donation as service
from ..services import donor as donor_service
from ..services import staff as staff_service

router = APIRouter(prefix="/donations", tags=["Donations"])

VIEW_ALL_ROLES = (Role.admin, Role.staff, Role.doctor)


@router.post(
    "/",
    response_model=DonationResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.admin, Role.staff))],
)
def create_donation(
    data: DonationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    staff_profile = staff_service.get_by_user_id(db, current_user.id)
    if not staff_profile:
        raise HTTPException(
            status_code=400,
            detail="Your account has no linked staff profile, so it cannot record a donation",
        )
    return service.create(db, data, collected_by_id=staff_profile.id)


@router.get(
    "/",
    response_model=list[DonationResponse],
    dependencies=[Depends(require_roles(*VIEW_ALL_ROLES))],
)
def list_donations(
    skip: int = 0,
    limit: int = 100,
    donor_id: int | None = None,
    screening_status: ScreeningStatus | None = None,
    db: Session = Depends(get_db),
):
    return service.get_all(db, skip, limit, donor_id, screening_status)


@router.get("/me", response_model=list[DonationResponse])
def get_my_donations(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    donor = donor_service.get_by_user_id(db, current_user.id)
    if not donor:
        raise HTTPException(status_code=404, detail="No donor profile linked to your account")
    return service.get_all(db, donor_id=donor.id)


@router.get(
    "/{donation_id}",
    response_model=DonationResponse,
    dependencies=[Depends(require_roles(*VIEW_ALL_ROLES))],
)
def get_donation(donation_id: int, db: Session = Depends(get_db)):
    donation = service.get_by_id(db, donation_id)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation


@router.put(
    "/{donation_id}/screening",
    response_model=DonationResponse,
    dependencies=[Depends(require_roles(Role.admin, Role.staff))],
)
def update_screening(
    donation_id: int, data: DonationScreeningUpdate, db: Session = Depends(get_db)
):
    donation = service.get_by_id(db, donation_id)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return service.update_screening(db, donation, data.screening_status)