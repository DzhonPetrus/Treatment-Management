from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class SurgeryType(Base):
    __tablename__ = "surgery_types"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    name = Column(String(100), unique=True)
    description = Column(Text)
    price = Column(Numeric(15,2))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    # surgery = relationship('Surgery', back_populates='surgery_type')