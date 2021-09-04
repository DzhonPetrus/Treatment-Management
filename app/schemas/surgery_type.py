from datetime import datetime as dt
from typing import Optional


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
