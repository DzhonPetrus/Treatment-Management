from datetime import datetime as dt
from typing import Optional, Any

from .treatment_type import *
from .user import *
from .inpatient import *
from .outpatient import *
from ..utils.schemaHelper import Base, as_form

class TreatmentBase(Base):
    treatment_no: Optional[str] = None
    inpatient_id: Optional[str] = None
    outpatient_id: Optional[str] = None

    room: Optional[str] = None
    quantity: Optional[float] = None
    physician_id: str

    treatment_type_id: str
    description: str

    professional_fee: Optional[float] = None
    session_no: Optional[int] = None
    session_datetime: Optional[dt] = None
    drug: Optional[str] = None
    dose: Optional[str] = None
    next_schedule: Optional[dt] = None
    comments: Optional[str] = None

    status: Optional[str] = None
    is_active: Optional[str] = None


@as_form
class CreateTreatment(TreatmentBase):
    pass


class Treatment(TreatmentBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None
    treatment_type: Optional[TreatmentTypeBase] = None
    inpatient: Optional[InPatientBase] = None
    outpatient: Optional[OutPatientBase] = None
    physician: Optional[User] = None


class OutTreatments(Base):
    data: List[Treatment]
    error: bool
    message: str

class OutTreatment(Base):
    data: Treatment
    error: bool
    message: str