from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel

from ..utils.schemaHelper import Base, as_form

class TreatmentTypeBase(Base):
    name: str
    room: str
    description: str
    price: float

    is_active: Optional[str] = None
    

@as_form
class CreateTreatmentType(TreatmentTypeBase):
    pass


class TreatmentType(TreatmentTypeBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

class OutTreatmentTypes(Base):
    data: List[TreatmentType]
    error: bool
    message: str

class OutTreatmentType(Base):
    data: TreatmentType
    error: bool
    message: str