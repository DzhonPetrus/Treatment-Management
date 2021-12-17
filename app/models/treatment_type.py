from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class TreatmentType(Base):
    __tablename__ = "treatment_types"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    name = Column(String(100), unique=True)
    room = Column(String(100))
    description = Column(Text)
    fee = Column(Numeric(15,2))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    treatments = relationship('Treatment', back_populates='treatment_type')