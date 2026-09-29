from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class BloodIssue(Base):
    __tablename__ = "bb_blood_issues"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    request_id: Mapped[int] = mapped_column(ForeignKey("bb_blood_requests.id"))
    blood_unit_id: Mapped[int] = mapped_column(ForeignKey("bb_blood_units.id"), unique=True)
    issued_by_id: Mapped[int] = mapped_column(ForeignKey("bb_staff.id"))

    issued_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    request = relationship("BloodRequest")
    blood_unit = relationship("BloodUnit")
    issued_by = relationship("Staff")