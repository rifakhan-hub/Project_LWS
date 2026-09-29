from sqlalchemy.orm import Session

from ..models.blood_component import BloodComponent


def get_all(db: Session, skip: int = 0, limit: int = 100, q: str | None = None):
    query = db.query(BloodComponent)
    if q:
        query = query.filter(BloodComponent.name.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, component_id: int):
    return db.query(BloodComponent).filter(BloodComponent.id == component_id).first()


def get_by_name(db: Session, name: str):
    return db.query(BloodComponent).filter(BloodComponent.name == name).first()


def create(db: Session, data):
    component = BloodComponent(**data.model_dump())
    db.add(component)
    db.commit()
    db.refresh(component)
    return component


def update(db: Session, component: BloodComponent, data):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(component, field, value)
    db.commit()
    db.refresh(component)
    return component


def delete(db: Session, component: BloodComponent):
    db.delete(component)
    db.commit()
    