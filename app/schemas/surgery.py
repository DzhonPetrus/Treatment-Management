from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel

from .surgery_type import *
from .patient import *
from ..utils.schemaHelper import Base, as_form

class SurgeryBase(Base):
    room: str
    patient_id: str
    surgery_type_id: str

    start_time: Optional[dt] = None
    end_time: Optional[dt] = None
    status: Optional[str] = None
    is_active: Optional[str] = None


@as_form
class CreateSurgery(SurgeryBase):
    pass


class Surgery(SurgeryBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None
    surgery_type: Optional[SurgeryTypeBase] = None
    patient: Optional[PatientBase] = None


class SurgeryOut(Base):
    data: List[Surgery]
    error: bool
    message: str