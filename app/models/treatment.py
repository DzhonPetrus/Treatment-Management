from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    patient_id = Column(String(36), ForeignKey("patients.id"))
    treatment_type_id = Column(String(36), ForeignKey("treatment_types.id"))
    user_id = Column(String(36), ForeignKey("users.id")) # DOCTOR IN CHARGE
    description = Column(Text)
    


    status = Column(String(100), default='PENDING')
    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    patient = relationship('Patient', back_populates='treatments')
    physician = relationship('User', back_populates='treatments')
    treatment_type = relationship('TreatmentType', back_populates='treatments')
  
