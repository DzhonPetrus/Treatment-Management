from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class LabResult(Base):
    __tablename__ = "lab_results"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    lab_request_id = Column(String(36), ForeignKey("lab_requests.id"))
    specimen = Column(String(100))
    result = Column(Text)
    reference = Column(String(100))
    unit = Column(String(100))
    detailed_result = Column(String(100))

    lab_result_no = Column(String(100))
    
    comments = Column(String(255))

    ordered = Column(String(150))
    dt_requested = Column(DateTime)
    dt_received = Column(DateTime)
    dt_reported = Column(DateTime)


    status = Column(String(100), default='PROCESSING')
    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    created_by = Column(String(36), ForeignKey("users.id"))
    updated_by = Column(String(36), ForeignKey("users.id"))

    creator = relationship('User', back_populates='lab_result_created', foreign_keys=[created_by])
    updator = relationship('User', back_populates='lab_result_updated', foreign_keys=[updated_by])

    lab_request = relationship('LabRequest', back_populates='lab_result')
    