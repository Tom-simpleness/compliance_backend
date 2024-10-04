# src/domain/value_objects/wallet_address.py
from dataclasses import dataclass

@dataclass(frozen=True)
class WalletAddress:
    value: str