from ..database import Base

from .surgery import *
from .surgery_type import *
from .lab_test import *
from .lab_results import *
from .lab_request import *
from .profile import *
from .treatment import *
from .treatment_type import *

from .patient import *




# RELATIONSHIPS
# SurgeryType.surgeries = relationship("Surgery", back_populates="surgery_type")

# Surgery.surgery_type = relationship("Surgery_Type", back_populates="surgeries")
