from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class BloodGroup(Base):
    __tablename__ = "bb_blood_groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(5), unique=True, index=True)