from datetime import date, datetime as dt
from typing import Optional, List


from ..utils.schemaHelper import Base, as_form



class PatientBase(Base):
    type : str
    first_name : str
    middle_name : Optional[str] = None
    last_name : str
    suffix_name : Optional[str] = None
    birth_date : date
    gender : str
    contact_no : str
    email : str
    blood_type : str
    picture : Optional[str] = None

    is_active: Optional[str] = None


@as_form
class CreatePatient(PatientBase):
    pass


class Patient(PatientBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

class OutPatients(Base):
    data: List[Patient]
    error: bool
    message: str

class OutPatient(Base):
    data: Patient
    error: bool
    message: str