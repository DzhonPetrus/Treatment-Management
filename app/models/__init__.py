from ..database import Base

from .surgery_in_charge import *
from .surgery import *
from .surgery_type import *

from .laboratory_service import *
from .laboratory_type import *

from .lab_test import *
from .lab_result import *
from .lab_request import *
from .profile import *

from .treatment_service import *
from .treatment import *
from .treatment_type import *

from .inpatient import *
from .outpatient import *
from .user import *




# RELATIONSHIPS
# SurgeryType.surgeries = relationship("Surgery", back_populates="surgery_type")

# Surgery.surgery_type = relationship("Surgery_Type", back_populates="surgeries")
