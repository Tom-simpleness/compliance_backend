# src/domain/repositories/whitelist_repository.py
from abc import ABC, abstractmethod

class IWhitelistRepository(ABC):
    @abstractmethod
    def is_whitelisted(self, wallet_address: str) -> bool:
        pass

    @abstractmethod
    def add_to_whitelist(self, wallet_address: str) -> None:
        pass

    @abstractmethod
    def remove_from_whitelist(self, wallet_address: str) -> None:
        pass