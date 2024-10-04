# src/domain/enums/kyc_level.py
from enum import Enum

class KycLevel(Enum):
    NONE = "NONE"
    PENDING = "PENDING"
    BASIC = "BASIC"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    FAILED = "FAILED"