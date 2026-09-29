from sqlalchemy.orm import Session

from ..models.donation import Donation, ScreeningStatus
from . import blood_unit as blood_unit_service


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    donor_id: int | None = None,
    screening_status: ScreeningStatus | None = None,
):
    query = db.query(Donation)
    if donor_id:
        query = query.filter(Donation.donor_id == donor_id)
    if screening_status:
        query = query.filter(Donation.screening_status == screening_status)
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, donation_id: int):
    return db.query(Donation).filter(Donation.id == donation_id).first()


def create(db: Session, data, collected_by_id: int) -> Donation:
    donation = Donation(**data.model_dump(), collected_by_id=collected_by_id)
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation


def update_screening(db: Session, donation: Donation, status: ScreeningStatus) -> Donation:
    donation.screening_status = status
    db.commit()
    db.refresh(donation)

    if status == ScreeningStatus.passed:
        blood_unit_service.create_from_donation(db, donation)

    return donation