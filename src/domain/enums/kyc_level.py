# src/domain/enums/kyc_level.py
from enum import Enum

class KycLevel(Enum):
    NONE = 0
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3