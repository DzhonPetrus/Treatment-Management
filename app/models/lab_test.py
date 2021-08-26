from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class LabTest(Base):
    __tablename__ = "lab_tests"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    name = Column(String(100))
    description = Column(Text)
    price = Column(Numeric(15,2))


    status = Column(String(100), default=text('ACTIVE'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))
