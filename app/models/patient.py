from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric, Date
from sqlalchemy.orm import relationship

from ..database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    type = Column(String(100))
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
    suffix_name = Column(String(100))
    birth_date = Column(Date)
    gender = Column(String(100))
    contact_no = Column(String(15))
    email = Column(String(100), unique=True)
    blood_type = Column(String(10))
    picture = Column(String(255))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    surgeries = relationship('Surgery', back_populates='patient')
    treatments = relationship('Treatment', back_populates='patient')
    lab_requests = relationship('LabRequest', back_populates='patient')