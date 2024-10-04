# src/domain/value_objects/address.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    street: str
    city: str
    country: str
    postal_code: str