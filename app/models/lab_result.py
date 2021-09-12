from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class LabResult(Base):
    __tablename__ = "lab_results"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    specimen = Column(String(100))
    result = Column(Text)
    reference = Column(String(100))
    unit = Column(String(100))
    detailed_result = Column(String(100))


    status = Column(String(100), default='PENDING')
    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    lab_requests = relationship('LabRequest', back_populates='lab_result')
    