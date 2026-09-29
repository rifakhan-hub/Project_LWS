from pydantic import BaseModel, ConfigDict


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    license_no: str
    phone: str
    user_id: int | None = None


class DoctorUpdate(DoctorCreate):
    pass


class DoctorResponse(BaseModel):
    id: int
    public_code: str
    name: str
    specialization: str
    license_no: str
    phone: str

    model_config = ConfigDict(from_attributes=True)