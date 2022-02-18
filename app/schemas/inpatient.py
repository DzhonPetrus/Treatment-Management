from datetime import date, datetime as dt
from typing import Optional, List


from ..utils.schemaHelper import Base, as_form



class InPatientBase(Base):
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
class CreateInPatient(InPatientBase):
    pass


class InPatient(InPatientBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

class OutInPatients(Base):
    data: List[InPatient]
    error: bool
    message: str

class OutInPatient(Base):
    data: InPatient
    error: bool
    message: str