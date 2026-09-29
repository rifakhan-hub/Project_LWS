from sqlalchemy.orm import Session

from ..models.doctor import Doctor


def _generate_public_code(db: Session) -> str:
    count = db.query(Doctor).count()
    return f"DOC-{count + 1:04d}"


def get_all(db: Session, skip: int = 0, limit: int = 100, q: str | None = None):
    query = db.query(Doctor)
    if q:
        query = query.filter(Doctor.name.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def create(db: Session, data) -> Doctor:
    doctor = Doctor(public_code=_generate_public_code(db), **data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def update(db: Session, doctor: Doctor, data) -> Doctor:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(doctor, field, value)
    db.commit()
    db.refresh(doctor)
    return doctor


def delete(db: Session, doctor: Doctor):
    db.delete(doctor)
    db.commit()