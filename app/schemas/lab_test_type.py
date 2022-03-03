from datetime import datetime as dt
from typing import Optional, List, Any
from pydantic import BaseModel
from ..utils.schemaHelper import Base, as_form


from .user import *
# from .lab_service_name import *

class Laboratory_typeBase(Base):
    lab_test_type_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    creator: Optional[UserBase] = None
    updator: Optional[UserBase] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

@as_form
class CreateLaboratory_type(Laboratory_typeBase):
    pass


class Laboratory_type(Laboratory_typeBase):
    id: str
    # lab_service_name: Optional[List[LabServiceNameBase]] = None
    lab_service_name: Optional[List[Any]] = None


class OutLaboratory_types(Base):
    data: List[Laboratory_type]
    error: bool
    message: str

class OutLaboratory_type(Base):
    data: Laboratory_type
    error: bool
    message: str