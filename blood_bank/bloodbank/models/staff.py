from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Staff(Base):
    __tablename__ = "bb_staff"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    public_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("bb_users.id"), unique=True, nullable=True
    )

    name: Mapped[str] = mapped_column(String(100))
    designation: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )