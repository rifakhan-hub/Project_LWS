from datetime import date

from pydantic import BaseModel, ConfigDict

from ..models.patient import PatientStatus


class PatientCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: str
    phone: str
    address: str | None = None
    user_id: int | None = None


class PatientAdminUpdate(PatientCreate):
    """Admin/staff: full update, including medical fields."""
    assigned_doctor_id: int | None = None
    diagnosis: str | None = None
    blood_group_needed_id: int | None = None
    units_required: int | None = None
    status: PatientStatus | None = None


class PatientDoctorUpdate(BaseModel):
    """Doctor: medical fields only."""
    assigned_doctor_id: int | None = None
    diagnosis: str | None = None
    blood_group_needed_id: int | None = None
    units_required: int | None = None
    status: PatientStatus | None = None


class PatientSelfUpdate(BaseModel):
    """Patient: their own non-medical fields only."""
    phone: str | None = None
    address: str | None = None


class PatientResponse(BaseModel):
    id: int
    public_code: str
    name: str
    date_of_birth: date
    gender: str
    phone: str
    address: str | None
    assigned_doctor_id: int | None
    diagnosis: str | None
    blood_group_needed_id: int | None
    units_required: int
    status: PatientStatus

    model_config = ConfigDict(from_attributes=True)

class PatientPublicView(BaseModel):
    
    public_code: str
    blood_group_needed_id: int | None
    units_required: int
    status: PatientStatus

    model_config = ConfigDict(from_attributes=True)