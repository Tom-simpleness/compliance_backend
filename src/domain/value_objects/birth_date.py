# src/domain/value_objects/birth_date.py
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class BirthDate:
    value: date