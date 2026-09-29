from datetime import date

from pydantic import BaseModel, ConfigDict

from ..models.blood_unit import UnitStatus


class BloodUnitStatusUpdate(BaseModel):
    status: UnitStatus


class BloodUnitResponse(BaseModel):
    id: int
    unit_code: str
    donation_id: int
    blood_group_id: int
    component_id: int
    collected_on: date
    expiry_date: date
    status: UnitStatus

    model_config = ConfigDict(from_attributes=True)