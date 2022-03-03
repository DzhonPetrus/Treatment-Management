from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base

class TreatmentServiceName(Base):
    __tablename__ = "treatment_service_name"    
    id = Column(String(36), primary_key=True, default=text('UUID()'))
    treatment_types_id = Column(String(36), ForeignKey("treatment_types.id"),nullable=False)
    treatment_service_name = Column(String(255),nullable=False,unique=True)
    description = Column(Text,nullable=False)
    unit_price = Column(Numeric(15,2),nullable=False)

    status = Column(String(255), nullable=False, default="ACTIVE")

    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))

    created_by = Column(String(36), ForeignKey("users.id"))
    updated_by = Column(String(36), ForeignKey("users.id"))

    creator = relationship('User', back_populates='treatment_service_created', foreign_keys=[created_by])
    updator = relationship('User', back_populates='treatment_service_updated', foreign_keys=[updated_by])

    treatments = relationship('Treatment', back_populates="treatment_service")

    treatment_type_info = relationship('Treatment_type', back_populates="treatment_service_name")

# ============================================================================================


