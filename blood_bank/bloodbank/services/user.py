from sqlalchemy.orm import Session

from ..models.user import Role, User
from ..schemas.user import UserCreate
from ..security import hash_password, verify_password


def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email.lower()).first()


def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create(db: Session, data: UserCreate):
    user = User(
        email=data.email.lower(),
        hashed_password=hash_password(data.password),
        role=Role(data.role),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str):
    """Return the user if email and password are correct, otherwise None."""
    user = get_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user