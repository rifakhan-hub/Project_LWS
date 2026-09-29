from sqlalchemy.orm import Session

from ..models.patient import Patient


def _generate_public_code(db: Session) -> str:
    count = db.query(Patient).count()
    return f"PAT-{count + 1:04d}"


def get_all(db: Session, skip: int = 0, limit: int = 100, q: str | None = None):
    query = db.query(Patient)
    if q:
        query = query.filter(Patient.name.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_by_user_id(db: Session, user_id: int):
    return db.query(Patient).filter(Patient.user_id == user_id).first()


def create(db: Session, data) -> Patient:
    patient = Patient(public_code=_generate_public_code(db), **data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def update(db: Session, patient: Patient, data) -> Patient:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient


def delete(db: Session, patient: Patient):
    db.delete(patient)
    db.commit()