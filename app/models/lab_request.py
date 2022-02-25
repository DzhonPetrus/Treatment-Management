from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base

# TODO:
# ADD LAB_REQUEST
# REMOVE INPATIENT_ID
# ADD INPATIENT_ID
# ADD OUTPATIENT_ID

class LabRequest(Base):
    __tablename__ = "lab_requests"

    id = Column(String(36), primary_key=True, default=text('UUID()'))

    # lab_test_id = Column(String(36), ForeignKey("lab_tests.id"))
    lab_service_id = Column(String(36), ForeignKey("laboratory_services.id"))

    inpatient_id = Column(String(36), ForeignKey("inpatients.id"))
    outpatient_id = Column(String(36), ForeignKey("outpatients.id"))
    quantity = Column(Numeric(15,2), nullable=False)

    lab_request_no = Column(String(100))

    is_active = Column(String(100), default='ACTIVE')
    status = Column(String(100), default='PENDING')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    created_by = Column(String(36), ForeignKey("users.id", name="fk_created_by"))
    updated_by = Column(String(36), ForeignKey("users.id", name="fk_updated_by"))

    creator = relationship('User', back_populates='lab_request_created', foreign_keys=[created_by])
    updator = relationship('User', back_populates='lab_request_updated', foreign_keys=[updated_by])

    lab_result = relationship('LabResult', back_populates='lab_request')

    # lab_test = relationship('LabTest', back_populates='lab_requests')
    laboratory_service = relationship('Laboratory_service', back_populates='lab_requests')

    inpatient = relationship('InPatient', back_populates='lab_requests')
    outpatient = relationship('OutPatient', back_populates='lab_requests')