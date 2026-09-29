import enum
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class ScreeningStatus(str, enum.Enum):
    pending = "pending"
    passed = "passed"
    failed = "failed"


class Donation(Base):
    __tablename__ = "bb_donations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    donor_id: Mapped[int] = mapped_column(ForeignKey("bb_donors.id"))
    collected_by_id: Mapped[int] = mapped_column(ForeignKey("bb_staff.id"))
    blood_group_id: Mapped[int] = mapped_column(ForeignKey("bb_blood_groups.id"))
    component_id: Mapped[int] = mapped_column(ForeignKey("bb_blood_components.id"))

    collection_date: Mapped[date] = mapped_column(Date)
    volume_ml: Mapped[float] = mapped_column(Float)
    screening_status: Mapped[ScreeningStatus] = mapped_column(
        Enum(ScreeningStatus), default=ScreeningStatus.pending
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    donor = relationship("Donor")
    collected_by = relationship("Staff")
    blood_group = relationship("BloodGroup")
    component = relationship("BloodComponent")