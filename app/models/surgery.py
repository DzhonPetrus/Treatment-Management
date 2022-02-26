from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Surgery(Base):
    __tablename__ = "surgeries"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    surgery_no = Column(String(100))
    inpatient_id = Column(String(36), ForeignKey("inpatients.id"))

    # TODO: room as FK to rooms table
    room = Column(String(100))

    surgery_service_id = Column(String(36), ForeignKey("surgery_services.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    head_surgeon_id = Column(String(36), ForeignKey("users.id"))
    description = Column(String(255))

    is_active = Column(String(100), default='ACTIVE')
    status = Column(String(100), default='PENDING')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    inpatient = relationship('InPatient', back_populates='surgeries')
    surgery_service = relationship("Surgery_service", back_populates="surgeries")

    in_charge = relationship('SurgeryInCharge', back_populates="surgery")
