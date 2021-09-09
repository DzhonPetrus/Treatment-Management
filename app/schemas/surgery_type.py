from datetime import datetime as dt
from typing import Optional, List


from ..utils.schemaHelper import Base, as_form



class SurgeryTypeBase(Base):
    name: str
    description: str
    price: float

    is_active: Optional[str]


@as_form
class CreateSurgeryType(SurgeryTypeBase):
    pass


class SurgeryType(SurgeryTypeBase):
    created_at: Optional[dt]
    updated_at: Optional[dt]

class SurgeryTypeOut(Base):
    data: List[SurgeryType]
    error: bool
    message: str