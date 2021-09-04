from datetime import datetime as dt
from typing import Optional
from pydantic import BaseModel

from ..utils.schemaHelper import Base, as_form

class Base(BaseModel):
    class Config():
        orm_mode = True


class TreatmentTypeBase(Base):
    name: str
    room: str
    description: str
    price: float

    is_active: Optional[str]
    

@as_form
class CreateTreatmentType(TreatmentTypeBase):
    pass


class TreatmentType(TreatmentTypeBase):
    created_at: Optional[dt]
    updated_at: Optional[dt]
