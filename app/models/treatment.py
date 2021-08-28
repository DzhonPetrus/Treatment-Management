from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class Treatment(Base):
    __tablename__ = "treatment"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    # patient_id = Column(String(36), ForeignKey("patients.id"))
    # profile_id = Column(String(36), ForeignKey("profile.id"))
    # treatment_type_id = Column(String(36), ForeignKey("treatment_types.id"))
    # lab_result_id = Column(String(36), ForeignKey("lab_result.id"))
    description = Column(Text)
    status = Column(String(100))
    


    status = Column(String(100), default='PENDING')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


  
