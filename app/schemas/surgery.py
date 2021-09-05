from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel

from .surgery_type import *
from ..utils.schemaHelper import Base, as_form
class Base(BaseModel):
    class Config():
        orm_mode = True


class SurgeryBase(Base):
    room: str
    patient_id: str
    surgery_type_id: str

    start_time: Optional[str]
    end_time: Optional[str]
    status: Optional[str]
    is_active: Optional[str]


@as_form
class CreateSurgery(SurgeryBase):
    pass


class Surgery(SurgeryBase):
    surgery_type: SurgeryType
    created_at: Optional[dt]
    updated_at: Optional[dt]

