from datetime import datetime as dt
from typing import Optional

from .treatment_type import *
from .user import *
from .patient import *
from ..utils.schemaHelper import Base, as_form

class TreatmentBase(Base):
    treatment_no: Optional[str] = None
    patient_id: str
    user_id: str
    treatment_type_id: str
    description: str

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
    patient: Optional[PatientBase] = None
    physician: Optional[User] = None


class OutTreatments(Base):
    data: List[Treatment]
    error: bool
    message: str

class OutTreatment(Base):
    data: Treatment
    error: bool
    message: str