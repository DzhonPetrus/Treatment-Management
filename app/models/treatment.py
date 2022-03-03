from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric, Float
from sqlalchemy.orm import relationship

from ..database import Base


class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    treatment_no = Column(String(100))
    room = Column(String(100))
    quantity = Column(Numeric(15,2), nullable=False)
    inpatient_id = Column(String(36), ForeignKey("inpatients.id"))
    outpatient_id = Column(String(36), ForeignKey("outpatients.id"))
    treatment_service_name_id = Column(String(36), ForeignKey("treatment_service_name.id"))
    physician_id = Column(String(36), ForeignKey("users.id")) # DOCTOR IN CHARGE
    description = Column(Text)
    cancellation_return = Column(Float)

    session_no = Column(Text)
    session_datetime = Column(DateTime)
    drug = Column(Text)
    dose = Column(Text)
    next_schedule = Column(DateTime)
    comments = Column(Text)
    


    status = Column(String(100), default='PENDING')
    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    created_by = Column(String(36), ForeignKey("users.id"))
    updated_by = Column(String(36), ForeignKey("users.id"))

    creator = relationship('User', back_populates='treatment_created', foreign_keys=[created_by])
    updator = relationship('User', back_populates='treatment_updated', foreign_keys=[updated_by])

    inpatient = relationship('InPatient', back_populates='treatments')
    outpatient = relationship('OutPatient', back_populates='treatments')
    physician = relationship('User', back_populates='treatments', foreign_keys=[physician_id])

    treatment_service = relationship('TreatmentServiceName', back_populates='treatments')
  
