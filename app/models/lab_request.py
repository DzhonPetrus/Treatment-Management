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
    lab_test_id = Column(String(36), ForeignKey("lab_tests.id"))
    # lab_result_id = Column(String(36), ForeignKey("lab_results.id"))
    inpatient_id = Column(String(36), ForeignKey("inpatients.id"))
    outpatient_id = Column(String(36), ForeignKey("outpatients.id"))
    quantity = Column(Numeric(15,2), nullable=False)

    lab_request_no = Column(String(100))

    is_active = Column(String(100), default='ACTIVE')
    status = Column(String(100), default='PENDING')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    lab_result = relationship('LabResult', back_populates='lab_request')
    lab_test = relationship('LabTest', back_populates='lab_requests')

    inpatient = relationship('InPatient', back_populates='lab_requests')
    outpatient = relationship('OutPatient', back_populates='lab_requests')