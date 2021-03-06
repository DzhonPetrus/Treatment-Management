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


    lab_request_created = relationship("LabRequest", back_populates="creator", foreign_keys='LabRequest.created_by')
    lab_request_updated = relationship("LabRequest", back_populates="updator", foreign_keys='LabRequest.updated_by')

    lab_result_created = relationship("LabResult", back_populates="creator", foreign_keys='LabResult.created_by')
    lab_result_updated = relationship("LabResult", back_populates="updator", foreign_keys='LabResult.updated_by')

    lab_service_name_created = relationship("LabServiceName", back_populates="creator", foreign_keys='LabServiceName.created_by')
    lab_service_name_updated = relationship("LabServiceName", back_populates="updator", foreign_keys='LabServiceName.updated_by')
    lab_test_type_created = relationship("Laboratory_type", back_populates="creator", foreign_keys='Laboratory_type.created_by')
    lab_test_type_updated = relationship("Laboratory_type", back_populates="updator", foreign_keys='Laboratory_type.updated_by')

    treatment_service_created = relationship("TreatmentServiceName", back_populates="creator", foreign_keys='TreatmentServiceName.created_by')
    treatment_service_updated = relationship("TreatmentServiceName", back_populates="updator", foreign_keys='TreatmentServiceName.updated_by')
    treatment_type_created = relationship("Treatment_type", back_populates="creator", foreign_keys='Treatment_type.created_by')
    treatment_type_updated = relationship("Treatment_type", back_populates="updator", foreign_keys='Treatment_type.updated_by')


    surgery_service_created = relationship("Surgery_service", back_populates="creator", foreign_keys='Surgery_service.created_by')
    surgery_service_updated = relationship("Surgery_service", back_populates="updator", foreign_keys='Surgery_service.updated_by')
    surgery_type_created = relationship("Surgery_type", back_populates="creator", foreign_keys='Surgery_type.created_by')
    surgery_type_updated = relationship("Surgery_type", back_populates="updator", foreign_keys='Surgery_type.updated_by')

    surgery_created = relationship("Surgery", back_populates="creator", foreign_keys='Surgery.created_by')
    surgery_updated = relationship("Surgery", back_populates="updator", foreign_keys='Surgery.updated_by')
    head_surgeries = relationship("Surgery", back_populates="head_surgeon", foreign_keys='Surgery.head_surgeon_id')

    handled_surgeries = relationship("SurgeryInCharge", back_populates="in_charge")

    treatment_created = relationship("Treatment", back_populates="creator", foreign_keys='Treatment.created_by')
    treatment_updated = relationship("Treatment", back_populates="updator", foreign_keys='Treatment.updated_by')
    treatments = relationship("Treatment", back_populates="physician", foreign_keys='Treatment.physician_id')