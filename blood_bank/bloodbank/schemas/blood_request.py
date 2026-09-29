from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..models.blood_request import RequestStatus, UrgencyLevel


class BloodRequestCreate(BaseModel):
    patient_id: int
    blood_group_id: int
    component_id: int
    units_requested: int = Field(gt=0)
    urgency: UrgencyLevel = UrgencyLevel.normal
    # requested_by_id is NOT here — set from the logged-in doctor, not the client


class BloodRequestStatusUpdate(BaseModel):
    """Staff/admin: approve or reject a pending request."""
    status: RequestStatus


class BloodRequestResponse(BaseModel):
    id: int
    patient_id: int
    requested_by_id: int
    blood_group_id: int
    component_id: int
    units_requested: int
    urgency: UrgencyLevel
    status: RequestStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)