from datetime import datetime as dt
from typing import Optional, List


from ..utils.schemaHelper import Base, as_form



class SurgeryTypeBase(Base):
    name: str
    description: str
    price: float

    is_active: Optional[str] = None


@as_form
class CreateSurgeryType(SurgeryTypeBase):
    pass


class SurgeryType(SurgeryTypeBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

class OutSurgeryTypes(Base):
    data: List[SurgeryType]
    error: bool
    message: str

class OutSurgeryType(Base):
    data: SurgeryType
    error: bool
    message: str