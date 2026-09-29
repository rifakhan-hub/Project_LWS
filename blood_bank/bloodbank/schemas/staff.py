from pydantic import BaseModel, ConfigDict


class StaffCreate(BaseModel):
    name: str
    designation: str
    phone: str
    user_id: int | None = None


class StaffUpdate(StaffCreate):
    pass


class StaffResponse(BaseModel):
    id: int
    public_code: str
    name: str
    designation: str
    phone: str

    model_config = ConfigDict(from_attributes=True)