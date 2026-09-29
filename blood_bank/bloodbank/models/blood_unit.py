import enum
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class UnitStatus(str, enum.Enum):
    available = "available"
    reserved = "reserved"
    issued = "issued"
    expired = "expired"
    discarded = "discarded"


class BloodUnit(Base):
    __tablename__ = "bb_blood_units"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    unit_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)

    donation_id: Mapped[int] = mapped_column(ForeignKey("bb_donations.id"), unique=True)
    blood_group_id: Mapped[int] = mapped_column(ForeignKey("bb_blood_groups.id"))
    component_id: Mapped[int] = mapped_column(ForeignKey("bb_blood_components.id"))

    collected_on: Mapped[date] = mapped_column(Date)
    expiry_date: Mapped[date] = mapped_column(Date)
    status: Mapped[UnitStatus] = mapped_column(Enum(UnitStatus), default=UnitStatus.available)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    donation = relationship("Donation")
    blood_group = relationship("BloodGroup")
    component = relationship("BloodComponent")