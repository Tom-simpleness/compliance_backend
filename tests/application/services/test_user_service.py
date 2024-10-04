# tests/application/services/test_user_service.py
import unittest
from uuid import UUID, uuid4
from src.domain.entities.identity import Identity
from src.domain.value_objects.address import Address
from src.domain.value_objects.birth_date import BirthDate
from src.domain.entities.document import Document
from src.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from src.infrastructure.repositories.in_memory_whitelist_repository import InMemoryWhitelistRepository
from src.application.services.user_service import UserService

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_repository = InMemoryUserRepository()
        self.whitelist_repository = InMemoryWhitelistRepository()
        self.service = UserService(self.user_repository, self.whitelist_repository)
        self.identity = Identity("John", "Doe", Address("123 Main St", "Anytown", "USA", "12345"), BirthDate("1990-01-01"))
        self.wallet_address = "0x1234567890123456789012345678901234567890"

    def test_create_user(self):
        self.whitelist_repository.add_to_whitelist(self.wallet_address)
        user = self.service.create_user(self.identity, self.wallet_address)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.identity, self.identity)
        self.assertEqual(user.wallet_address.value, self.wallet_address)

    def test_get_user(self):
        self.whitelist_repository.add_to_whitelist(self.wallet_address)
        created_user = self.service.create_user(self.identity, self.wallet_address)
        retrieved_user = self.service.get_user(created_user.id)
        self.assertEqual(retrieved_user, created_user)

    def test_update_user_risk_score(self):
        self.whitelist_repository.add_to_whitelist(self.wallet_address)
        user = self.service.create_user(self.identity, self.wallet_address)
        self.service.update_user_risk_score(user.id, 75)
        updated_user = self.service.get_user(user.id)
        self.assertEqual(updated_user.risk_score.score, 75)

    def test_add_document_to_user(self):
        self.whitelist_repository.add_to_whitelist(self.wallet_address)
        user = self.service.create_user(self.identity, self.wallet_address)
        document = Document(uuid4(), "Passport", "123456", "2030-01-01")
        self.service.add_document_to_user(user.id, document)
        updated_user = self.service.get_user(user.id)
        self.assertEqual(len(updated_user.documents), 1)
        self.assertEqual(updated_user.documents[0], document)

if __name__ == '__main__':
    unittest.main()