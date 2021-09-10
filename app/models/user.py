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