from sqlalchemy.orm import Session

from ..models.blood_group import BloodGroup
from ..schemas.blood_group import BloodGroupCreate, BloodGroupUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100, q: str | None = None):
    query = db.query(BloodGroup)
    if q:
        query = query.filter(BloodGroup.name.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, blood_group_id: int):
    return db.query(BloodGroup).filter(BloodGroup.id == blood_group_id).first()


def get_by_name(db: Session, name: str):
    return db.query(BloodGroup).filter(BloodGroup.name == name).first()


def create(db: Session, data: BloodGroupCreate):
    new_group = BloodGroup(name=data.name)
    db.add(new_group)      # stage it
    db.commit()            # save it to the database
    db.refresh(new_group)  # reload it so we get the generated id
    return new_group


def update(db: Session, blood_group: BloodGroup, data: BloodGroupUpdate):
    blood_group.name = data.name
    db.commit()
    db.refresh(blood_group)
    return blood_group


def delete(db: Session, blood_group: BloodGroup):
    db.delete(blood_group)
    db.commit()