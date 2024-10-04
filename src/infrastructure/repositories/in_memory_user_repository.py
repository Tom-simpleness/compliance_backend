# src/infrastructure/repositories/in_memory_user_repository.py
from uuid import UUID
from src.domain.repositories.user_repository import IUserRepository
from src.domain.aggregates.user import User
from src.domain.value_objects.wallet_address import WalletAddress

class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._users = {}

    def get_by_id(self, user_id: UUID) -> User:
        user = self._users.get(user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found")
        return user

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def delete(self, user_id: UUID) -> None:
        if user_id in self._users:
            del self._users[user_id]

    def get_by_wallet_address(self, wallet_address: str) -> User:
        for user in self._users.values():
            if user.wallet_address == WalletAddress(wallet_address):
                return user
        raise ValueError(f"User with wallet address {wallet_address} not found")