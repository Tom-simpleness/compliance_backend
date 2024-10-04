# src/domain/repositories/user_repository.py
from abc import ABC, abstractmethod
from uuid import UUID
from ..aggregates.user import User

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    def get_by_wallet_address(self, wallet_address: str) -> User:
        pass