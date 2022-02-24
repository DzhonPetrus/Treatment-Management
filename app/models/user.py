from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    email = Column(String(100), unique=True)
    user_type = Column(String(100))
    password = Column(String(255))
    user_profile_id = Column(String(36), ForeignKey("user_profiles.id"))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    user_profile = relationship("Profile", back_populates="user_account")
    treatments = relationship("Treatment", back_populates="physician")

    handled_surgeries = relationship("SurgeryInCharge", back_populates="in_charge")

    lab_request_created = relationship("LabRequest", back_populates="creator", foreign_keys='LabRequest.created_by')
    lab_request_updated = relationship("LabRequest", back_populates="updator", foreign_keys='LabRequest.updated_by')
    lab_result_created = relationship("LabResult", back_populates="creator", foreign_keys='LabResult.created_by')
    lab_result_updated = relationship("LabResult", back_populates="updator", foreign_keys='LabResult.updated_by')