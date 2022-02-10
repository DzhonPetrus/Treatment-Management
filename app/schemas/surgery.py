from datetime import datetime as dt
from typing import Optional, List, Any
from pydantic import BaseModel

from .user import UserBase
from .surgery_type import *
from .patient import *
from ..utils.schemaHelper import Base, as_form

class SurgeryBase(Base):
    surgery_no: Optional[str] = None
    room: Optional[str] = None
    patient_id: Optional[str] = None
    surgery_type_id: Optional[str] = None

    in_charge: Optional[Any] = None

    start_time: Optional[dt] = None
    end_time: Optional[dt] = None
    status: Optional[str] = None
    is_active: Optional[str] = None


@as_form
class CreateSurgery(SurgeryBase):
    pass


class InCharge(Base):
    in_charge_id: Optional[Any] = None
    surgery_id: Optional[Any] = None
    professional_fee: Optional[Any] = None
    in_charge: Optional[UserBase] = None


class Surgery(SurgeryBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None
    surgery_type: Optional[SurgeryTypeBase] = None
    in_charge: Optional[List[InCharge]] = None
    patient: Optional[PatientBase] = None


class OutSurgeries(Base):
    data: List[Surgery]
    error: bool
    message: str

class OutSurgery(Base):
    data: Surgery
    error: bool
    message: str