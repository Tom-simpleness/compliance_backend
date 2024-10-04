# src/domain/services/identity_verification_service.py
from abc import ABC, abstractmethod
from ..entities.identity import Identity

class IIdentityVerificationService(ABC):
    @abstractmethod
    def verify_identity(self, identity: Identity) -> bool:
        """
        Verify the identity of a user.
        
        :param identity: The identity to verify
        :return: True if the identity is verified, False otherwise
        """
        pass