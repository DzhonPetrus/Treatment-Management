from uuid import uuid4
from sqlalchemy import Column, String, DateTime, text, ForeignKey, Date
from sqlalchemy.orm import relationship

from ..database import Base


class Profile(Base):
    __tablename__ = "user_profiles"

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    # department_id = Column(String(36), ForeignKey("departments.id"))
    department = Column(String(100))
    position = Column(String(100))
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
    suffix_name = Column(String(100))
    birth_date = Column(String(100))
    photo_url = Column(String(255))


    is_active = Column(String(100), default='ACTIVE')
    created_at = Column(DateTime, default=text('NOW()'))
    updated_at = Column(DateTime, default=text('NOW()'), onupdate=text('NOW()'))


    # department = relationship('Department', back_populates='user_profile')
    user_account = relationship('User', back_populates='user_profile')