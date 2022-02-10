from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel
from ..utils.schemaHelper import Base, as_form
from .lab_result import *
from .lab_test import *
from .patient import *

class LabRequestBase(Base):
    patient_id: str
    # lab_test_id: str
    # lab_result_id: str

    lab_test_id: Optional[str] = None
    lab_request_no: Optional[str] = None

    status: Optional[str] = None
    is_active: Optional[str] = None


@as_form
class CreateLabRequest(LabRequestBase):
    pass


class LabRequest(LabRequestBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None
    # lab_result: Optional[LabResultBase] = None
    lab_test: Optional[LabTestBase] = None
    patient: Optional[PatientBase] = None


class OutLabRequests(Base):
    data: List[LabRequest]
    error: bool
    message: str

class OutLabRequest(Base):
    data: LabRequest
    error: bool
    message: str