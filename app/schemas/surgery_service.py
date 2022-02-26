from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel
from ..utils.schemaHelper import Base, as_form


from .user import *
from .surgery_type import *

class Surgery_serviceBase(Base):
    surgery_type_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    fee: Optional[float] = None
    is_active: Optional[str] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    creator: Optional[UserBase] = None
    updator: Optional[UserBase] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None
    surgery_type: Optional[Surgery_typeBase] = None

@as_form
class CreateSurgery_service(Surgery_serviceBase):
    pass


class Surgery_service(Surgery_serviceBase):
    id: str


class OutSurgery_services(Base):
    data: List[Surgery_service]
    error: bool
    message: str

class OutSurgery_service(Base):
    data: Surgery_service
    error: bool
    message: str
