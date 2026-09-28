from pydantic import BaseModel, ConfigDict, field_validator

VALID_GROUPS = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}


class BloodGroupCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def check_name(cls, value: str) -> str:
        value = value.strip().upper()
        if value not in VALID_GROUPS:
            raise ValueError(f"name must be one of {sorted(VALID_GROUPS)}")
        return value


class BloodGroupUpdate(BloodGroupCreate):
    pass  # same rules as create for now


class BloodGroupResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)