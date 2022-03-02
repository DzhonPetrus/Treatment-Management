from datetime import datetime as dt
from typing import Optional, List, Any
from pydantic import BaseModel
from ..utils.schemaHelper import Base, as_form


from .user import *
# from .surgery_service import *

class Surgery_typeBase(Base):
    surgery_type_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[str] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    creator: Optional[UserBase] = None
    updator: Optional[UserBase] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

@as_form
class CreateSurgery_type(Surgery_typeBase):
    pass


class Surgery_type(Surgery_typeBase):
    id: str
    # surgery_services: Optional[List[Surgery_serviceBase]] = None
    surgery_services: Optional[List[Any]] = None


class OutSurgery_types(Base):
    data: List[Surgery_type]
    error: bool
    message: str

class OutSurgery_type(Base):
    data: Surgery_type
    error: bool
    message: str