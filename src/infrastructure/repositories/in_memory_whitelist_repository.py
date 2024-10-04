# src/infrastructure/repositories/in_memory_whitelist_repository.py
from src.domain.repositories.whitelist_repository import IWhitelistRepository

class InMemoryWhitelistRepository(IWhitelistRepository):
    def __init__(self):
        self._whitelisted_addresses = set()

    def is_whitelisted(self, wallet_address: str) -> bool:
        return wallet_address in self._whitelisted_addresses

    def add_to_whitelist(self, wallet_address: str) -> None:
        self._whitelisted_addresses.add(wallet_address)

    def remove_from_whitelist(self, wallet_address: str) -> None:
        self._whitelisted_addresses.discard(wallet_address)