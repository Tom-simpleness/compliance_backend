# src/application/services/wallet_whitelist_service.py

from ...domain.value_objects.wallet_address import WalletAddress

class WalletWhitelistService:
    def __init__(self, whitelist_repository):
        self.whitelist_repository = whitelist_repository

    def is_whitelisted(self, wallet_address: WalletAddress) -> bool:
        return self.whitelist_repository.is_whitelisted(wallet_address.value)