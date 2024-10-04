# src/domain/entities/document.py
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Document:
    id: uuid.UUID
    type: str
    number: str
    expiration_date: datetime