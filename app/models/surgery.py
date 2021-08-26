from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Surgery(Base):
    __tablename__ = "surgeries"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    # patient_id = Column(String(36), ForeignKey("patients.id"))
    # room_id = Column(String(36), ForeignKey("rooms.id"))
    # surgery_type_id = Column(String(36), ForeignKey("surgery_types.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)


    status = Column(String(100), default=text('PENDING'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    # patient = relationship('Patient', back_populates='surgeries')
    # room = relationship('Room', back_populates='surgeries')
    # surgery_type = relationship('Surgery_Type', back_populates='surgery')
