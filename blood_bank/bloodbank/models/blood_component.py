from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class BloodComponent(Base):
    __tablename__ = "bb_blood_components"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    shelf_life_days: Mapped[int]