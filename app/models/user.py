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

    handled_surgeries = relationship("SurgeryInCharge", back_populates="in_charge")

    lab_request_created = relationship("LabRequest", back_populates="creator", foreign_keys='LabRequest.created_by')
    lab_request_updated = relationship("LabRequest", back_populates="updator", foreign_keys='LabRequest.updated_by')

    lab_result_created = relationship("LabResult", back_populates="creator", foreign_keys='LabResult.created_by')
    lab_result_updated = relationship("LabResult", back_populates="updator", foreign_keys='LabResult.updated_by')

    laboratory_service_created = relationship("Laboratory_service", back_populates="creator", foreign_keys='Laboratory_service.created_by')
    laboratory_service_updated = relationship("Laboratory_service", back_populates="updator", foreign_keys='Laboratory_service.updated_by')
    laboratory_type_created = relationship("Laboratory_type", back_populates="creator", foreign_keys='Laboratory_type.created_by')
    laboratory_type_updated = relationship("Laboratory_type", back_populates="updator", foreign_keys='Laboratory_type.updated_by')



    treatment_created = relationship("Treatment", back_populates="creator", foreign_keys='Treatment.created_by')
    treatment_updated = relationship("Treatment", back_populates="updator", foreign_keys='Treatment.updated_by')
    treatments = relationship("Treatment", back_populates="physician", foreign_keys='Treatment.physician_id')