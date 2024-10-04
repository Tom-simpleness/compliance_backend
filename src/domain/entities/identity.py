# src/domain/entities/identity.py
from dataclasses import dataclass
from ..value_objects.address import Address
from ..value_objects.birth_date import BirthDate

@dataclass
class Identity:
    first_name: str
    last_name: str
    address: Address
    birth_date: BirthDate