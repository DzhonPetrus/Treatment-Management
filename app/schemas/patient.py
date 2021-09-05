from datetime import datetime as dt
from typing import Optional


from ..utils.schemaHelper import Base, as_form



class PatientBase(Base):
    type : str
    first_name : str
    middle_name : Optional[str]
    last_name : str
    suffix_name : Optional[str]
    birth_date : str
    gender : str
    contact_no : str
    email : str
    blood_type : str
    picture : Optional[str]

    is_active: Optional[str]


@as_form
class CreatePatient(PatientBase):
    pass


class Patient(PatientBase):
    created_at: Optional[dt]
    updated_at: Optional[dt]