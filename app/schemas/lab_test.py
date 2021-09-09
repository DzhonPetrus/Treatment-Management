from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel

from ..utils.schemaHelper import Base, as_form

class LabTestBase(Base):  
    name: str
    description: str
    price: float

    is_active: Optional[str] = None


@as_form
class CreateLabTest(LabTestBase):
    pass


class LabTest(LabTestBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

class OutLabTests(Base):
    data: List[LabTest]
    error: bool
    message: str

class OutLabTest(Base):
    data: LabTest
    error: bool
    message: str