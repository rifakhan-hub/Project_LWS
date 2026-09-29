from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BloodIssueCreate(BaseModel):
    request_id: int
    blood_unit_id: int
    # issued_by_id is NOT here — set from the logged-in staff member, not the client


class BloodIssueResponse(BaseModel):
    id: int
    request_id: int
    blood_unit_id: int
    issued_by_id: int
    issued_at: datetime

    model_config = ConfigDict(from_attributes=True)