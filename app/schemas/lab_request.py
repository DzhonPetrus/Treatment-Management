from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel
from ..utils.schemaHelper import Base, as_form
from .lab_result import *
from .lab_test import *

from .inpatient import *
from .outpatient import *

from .laboratory_service import *

from .user import *

class LabRequestBase(Base):
    inpatient_id: Optional[str] = None
    outpatient_id: Optional[str] = None
    # lab_test_id: str
    # lab_result_id: str
    quantity: Optional[float] = None

    # lab_test_id: Optional[str] = None
    laboratory_service_id: Optional[str] = None

    lab_request_no: Optional[str] = None

    status: Optional[str] = None
    is_active: Optional[str] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    creator: Optional[UserBase] = None
    updator: Optional[UserBase] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

@as_form
class CreateLabRequest(LabRequestBase):
    pass


class LabRequest(LabRequestBase):
    id: str
    # lab_result: Optional[LabResultBase] = None
    # lab_test: Optional[LabTestBase] = None
    laboratory_service: Optional[Laboratory_serviceBase] = None
    inpatient: Optional[InPatientBase] = None
    outpatient: Optional[OutPatientBase] = None


class OutLabRequests(Base):
    data: List[LabRequest]
    error: bool
    message: str

class OutLabRequest(Base):
    data: LabRequest
    error: bool
    message: str