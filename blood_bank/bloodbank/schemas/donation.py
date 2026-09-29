from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from ..models.donation import ScreeningStatus


class DonationCreate(BaseModel):
    donor_id: int
    blood_group_id: int
    component_id: int
    collection_date: date
    volume_ml: float = Field(gt=0)
    # collected_by_id is NOT here — it's set from the logged-in staff user, not the client


class DonationScreeningUpdate(BaseModel):
    """Staff updates only this, after lab results come in."""
    screening_status: ScreeningStatus


class DonationResponse(BaseModel):
    id: int
    donor_id: int
    collected_by_id: int
    blood_group_id: int
    component_id: int
    collection_date: date
    volume_ml: float
    screening_status: ScreeningStatus

    model_config = ConfigDict(from_attributes=True)
    