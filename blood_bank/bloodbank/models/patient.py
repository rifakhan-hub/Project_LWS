import enum
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class PatientStatus(str, enum.Enum):
    admitted = "admitted"
    under_treatment = "under_treatment"
    discharged = "discharged"


class Patient(Base):
    __tablename__ = "bb_patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    public_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("bb_users.id"), unique=True, nullable=True
    )

    # Non-medical fields — the patient can edit these themself
    name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[date] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String(10))
    phone: Mapped[str] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Medical fields — only a doctor can edit these
    assigned_doctor_id: Mapped[int | None] = mapped_column(
        ForeignKey("bb_doctors.id"), nullable=True
    )
    diagnosis: Mapped[str | None] = mapped_column(String(255), nullable=True)
    blood_group_needed_id: Mapped[int | None] = mapped_column(
        ForeignKey("bb_blood_groups.id"), nullable=True
    )
    units_required: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[PatientStatus] = mapped_column(
        Enum(PatientStatus), default=PatientStatus.admitted
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    assigned_doctor = relationship("Doctor")
    blood_group_needed = relationship("BloodGroup")