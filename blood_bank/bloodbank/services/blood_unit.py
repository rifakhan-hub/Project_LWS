from datetime import date, timedelta

from sqlalchemy.orm import Session

from ..models.blood_component import BloodComponent
from ..models.blood_unit import BloodUnit, UnitStatus
from ..models.donation import Donation


def _generate_unit_code(db: Session) -> str:
    count = db.query(BloodUnit).count()
    return f"BU-{count + 1:05d}"


def create_from_donation(db: Session, donation: Donation) -> BloodUnit:
    """Called when a donation's screening passes. Builds the unit and computes expiry."""
    component = db.query(BloodComponent).filter(
        BloodComponent.id == donation.component_id
    ).first()

    expiry_date = donation.collection_date + timedelta(days=component.shelf_life_days)

    unit = BloodUnit(
        unit_code=_generate_unit_code(db),
        donation_id=donation.id,
        blood_group_id=donation.blood_group_id,
        component_id=donation.component_id,
        collected_on=donation.collection_date,
        expiry_date=expiry_date,
        status=UnitStatus.available,
    )
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    blood_group_id: int | None = None,
    component_id: int | None = None,
    status: UnitStatus | None = None,
):
    query = db.query(BloodUnit)
    if blood_group_id:
        query = query.filter(BloodUnit.blood_group_id == blood_group_id)
    if component_id:
        query = query.filter(BloodUnit.component_id == component_id)
    if status:
        query = query.filter(BloodUnit.status == status)
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, unit_id: int):
    return db.query(BloodUnit).filter(BloodUnit.id == unit_id).first()


def update_status(db: Session, unit: BloodUnit, status: UnitStatus) -> BloodUnit:
    unit.status = status
    db.commit()
    db.refresh(unit)
    return unit