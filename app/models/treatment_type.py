from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


# LABORATORY
class Treatment_type(Base):
    __tablename__ = "treatment_types"    
    id = Column(String(36), primary_key=True, default=text('UUID()'))
    treatment_type_name = Column(String(255),nullable=False,unique=True)
    description = Column(Text,nullable=False)

    status = Column(String(255), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    created_by = Column(String(36), ForeignKey("users.id"))
    updated_by = Column(String(36), ForeignKey("users.id"))

    creator = relationship('User', back_populates='treatment_type_created', foreign_keys=[created_by])
    updator = relationship('User', back_populates='treatment_type_updated', foreign_keys=[updated_by])

    treatment_service_name = relationship("TreatmentServiceName", back_populates="treatment_type_info")