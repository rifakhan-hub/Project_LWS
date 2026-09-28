from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Donor(Base):
    __tablename__ = "bb_donors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    public_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)

    # Optional: a walk-in donor added by staff may not have a login yet
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("bb_users.id"), unique=True, nullable=True
    )

    name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[date] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String(10))
    phone: Mapped[str] = mapped_column(String(20))
    weight_kg: Mapped[float]
    blood_group_id: Mapped[int] = mapped_column(ForeignKey("bb_blood_groups.id"))
    last_donation_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_eligible: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    blood_group = relationship("BloodGroup")