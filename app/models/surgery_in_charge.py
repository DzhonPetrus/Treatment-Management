from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class SurgeryInCharge(Base):
    __tablename__ = "surgery_in_charge"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    professional_fee = Column(Numeric(15,2))
    # is_head_surgeon = Column(Boolean)


    in_charge_id = Column(ForeignKey('users.id'))
    surgery_id = Column(ForeignKey('surgeries.id'))

    in_charge = relationship('User', back_populates="handled_surgeries")
    surgery = relationship("Surgery", back_populates="in_charge")
