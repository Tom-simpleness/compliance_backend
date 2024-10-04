# src/application/services/user_service.py
from uuid import UUID, uuid4
from src.domain.repositories.user_repository import IUserRepository
from src.domain.repositories.whitelist_repository import IWhitelistRepository
from src.domain.services.identity_verification_service import IIdentityVerificationService
from src.domain.aggregates.user import User
from src.domain.entities.identity import Identity
from src.domain.value_objects.wallet_address import WalletAddress
from src.domain.enums.kyc_level import KycLevel

class UserService:
    def __init__(self, 
                 user_repository: IUserRepository, 
                 whitelist_repository: IWhitelistRepository,
                 identity_verification_service: IIdentityVerificationService):
        self._user_repository = user_repository
        self._whitelist_repository = whitelist_repository
        self._identity_verification_service = identity_verification_service

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

    def request_identity_verification(self, user_id: UUID) -> None:
        user = self._user_repository.get_by_id(user_id)
        if user.kyc_level != KycLevel.NONE and user.kyc_level != KycLevel.FAILED:
            raise ValueError("User verification has already been initiated or completed")

        user.update_kyc_level(KycLevel.PENDING)
        self._user_repository.save(user)

        # Dans un système réel, ceci pourrait être un appel asynchrone ou une tâche en arrière-plan
        verification_result = self._identity_verification_service.verify_identity(user.identity)
        
        if verification_result:
            user.update_kyc_level(KycLevel.BASIC)
        else:
            user.update_kyc_level(KycLevel.FAILED)
        
        self._user_repository.save(user)

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