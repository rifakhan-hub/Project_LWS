from sqlalchemy.orm import Session

from ..models.donor import Donor


def _generate_public_code(db: Session) -> str:
    count = db.query(Donor).count()
    return f"DON-{count + 1:04d}"


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    q: str | None = None,
    blood_group_id: int | None = None,
):
    query = db.query(Donor)
    if q:
        query = query.filter(Donor.name.ilike(f"%{q}%"))
    if blood_group_id:
        query = query.filter(Donor.blood_group_id == blood_group_id)
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, donor_id: int):
    return db.query(Donor).filter(Donor.id == donor_id).first()


def get_by_user_id(db: Session, user_id: int):
    return db.query(Donor).filter(Donor.user_id == user_id).first()


def create(db: Session, data) -> Donor:
    donor = Donor(public_code=_generate_public_code(db), **data.model_dump())
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor


def update(db: Session, donor: Donor, data) -> Donor:
    # exclude_unset=True: only touch fields the client actually sent
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(donor, field, value)
    db.commit()
    db.refresh(donor)
    return donor


def delete(db: Session, donor: Donor):
    db.delete(donor)
    db.commit()