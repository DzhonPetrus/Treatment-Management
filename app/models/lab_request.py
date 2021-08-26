from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

from ..database import Base


class LabRequest(Base):
    __tablename__ = "lab_request"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    

    status = Column(String(100), default=text('ACTIVE'))
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, onupdate=text('NOW()'))


    #lab_result
    #lab_test