# tests/infrastructure/repositories/test_in_memory_user_repository.py
import unittest
from uuid import uuid4
from src.domain.aggregates.user import User
from src.domain.entities.identity import Identity
from src.domain.value_objects.address import Address
from src.domain.value_objects.birth_date import BirthDate
from src.domain.value_objects.wallet_address import WalletAddress
from src.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository

class TestInMemoryUserRepository(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryUserRepository()
        self.user = User(
            id=uuid4(),
            identity=Identity("John", "Doe", Address("123 Main St", "Anytown", "USA", "12345"), BirthDate("1990-01-01")),
            wallet_address=WalletAddress("0x1234567890123456789012345678901234567890")
        )

    def test_save_and_get_by_id(self):
        self.repository.save(self.user)
        retrieved_user = self.repository.get_by_id(self.user.id)
        self.assertEqual(retrieved_user, self.user)

    def test_delete(self):
        self.repository.save(self.user)
        self.repository.delete(self.user.id)
        with self.assertRaises(ValueError):
            self.repository.get_by_id(self.user.id)

    def test_get_by_wallet_address(self):
        self.repository.save(self.user)
        retrieved_user = self.repository.get_by_wallet_address("0x1234567890123456789012345678901234567890")
        self.assertEqual(retrieved_user, self.user)