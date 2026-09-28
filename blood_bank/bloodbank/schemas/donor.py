from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class DonorCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: str
    phone: str
    weight_kg: float = Field(gt=0)
    blood_group_id: int
    user_id: int | None = None


class DonorAdminUpdate(DonorCreate):
    is_eligible: bool | None = None
    last_donation_date: date | None = None


class DonorSelfUpdate(BaseModel):
    """A donor may only touch these fields on their own profile."""
    phone: str | None = None
    weight_kg: float | None = Field(default=None, gt=0)


class DonorResponse(BaseModel):
    id: int
    public_code: str
    name: str
    date_of_birth: date
    gender: str
    phone: str
    weight_kg: float
    blood_group_id: int
    last_donation_date: date | None
    is_eligible: bool

    model_config = ConfigDict(from_attributes=True)