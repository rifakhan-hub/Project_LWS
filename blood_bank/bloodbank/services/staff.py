from sqlalchemy.orm import Session

from ..models.staff import Staff


def _generate_public_code(db: Session) -> str:
    count = db.query(Staff).count()
    return f"STF-{count + 1:04d}"


def get_all(db: Session, skip: int = 0, limit: int = 100, q: str | None = None):
    query = db.query(Staff)
    if q:
        query = query.filter(Staff.name.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, staff_id: int):
    return db.query(Staff).filter(Staff.id == staff_id).first()


def create(db: Session, data) -> Staff:
    staff = Staff(public_code=_generate_public_code(db), **data.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


def update(db: Session, staff: Staff, data) -> Staff:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(staff, field, value)
    db.commit()
    db.refresh(staff)
    return staff


def delete(db: Session, staff: Staff):
    db.delete(staff)
    db.commit()