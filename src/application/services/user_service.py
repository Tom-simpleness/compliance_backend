# src/application/services/user_service.py
from uuid import UUID, uuid4
from src.domain.repositories.user_repository import IUserRepository
from src.domain.repositories.whitelist_repository import IWhitelistRepository
from src.domain.aggregates.user import User
from src.domain.entities.identity import Identity
from src.domain.value_objects.wallet_address import WalletAddress

class UserService:
    def __init__(self, user_repository: IUserRepository, whitelist_repository: IWhitelistRepository):
        self._user_repository = user_repository
        self._whitelist_repository = whitelist_repository

    def create_user(self, identity: Identity, wallet_address: str) -> User:
        if not self._whitelist_repository.is_whitelisted(wallet_address):
            raise ValueError("Wallet address is not whitelisted")
        user = User(
            id=uuid4(),
            identity=identity,
            wallet_address=WalletAddress(wallet_address)
        )
        self._user_repository.save(user)
        return user

    def get_user(self, user_id: UUID) -> User:
        return self._user_repository.get_by_id(user_id)

    def update_user_risk_score(self, user_id: UUID, new_score: int) -> None:
        user = self._user_repository.get_by_id(user_id)
        user.update_risk_score(new_score)
        self._user_repository.save(user)

    def add_document_to_user(self, user_id: UUID, document) -> None:
        user = self._user_repository.get_by_id(user_id)
        user.add_document(document)
        self._user_repository.save(user)