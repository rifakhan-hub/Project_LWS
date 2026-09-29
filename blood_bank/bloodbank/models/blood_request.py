import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class RequestStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    fulfilled = "fulfilled"


class UrgencyLevel(str, enum.Enum):
    normal = "normal"
    urgent = "urgent"
    critical = "critical"


class BloodRequest(Base):
    __tablename__ = "bb_blood_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    patient_id: Mapped[int] = mapped_column(ForeignKey("bb_patients.id"))
    requested_by_id: Mapped[int] = mapped_column(ForeignKey("bb_doctors.id"))
    blood_group_id: Mapped[int] = mapped_column(ForeignKey("bb_blood_groups.id"))
    component_id: Mapped[int] = mapped_column(ForeignKey("bb_blood_components.id"))

    units_requested: Mapped[int] = mapped_column(Integer)
    urgency: Mapped[UrgencyLevel] = mapped_column(Enum(UrgencyLevel), default=UrgencyLevel.normal)
    status: Mapped[RequestStatus] = mapped_column(Enum(RequestStatus), default=RequestStatus.pending)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    patient = relationship("Patient")
    requested_by = relationship("Doctor")
    blood_group = relationship("BloodGroup")
    component = relationship("BloodComponent")