from pydantic import BaseModel, ConfigDict, Field


class BloodComponentCreate(BaseModel):
    name: str
    shelf_life_days: int = Field(gt=0)


class BloodComponentUpdate(BloodComponentCreate):
    pass


class BloodComponentResponse(BaseModel):
    id: int
    name: str
    shelf_life_days: int

    model_config = ConfigDict(from_attributes=True)