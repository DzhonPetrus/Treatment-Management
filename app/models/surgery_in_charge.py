from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class SurgeryInCharge(Base):
    __tablename__ = "surgery_in_charge"

    professional_fee = Column(Numeric(15,2))


    in_charge_id = Column(ForeignKey('users.id'), primary_key=True)
    surgery_id = Column(ForeignKey('surgeries.id'), primary_key=True)

    in_charge = relationship('User', back_populates="handled_surgeries")
    surgery = relationship("Surgery", back_populates="in_charge")
