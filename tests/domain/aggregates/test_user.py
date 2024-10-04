# tests/domain/aggregates/test_user.py
import unittest
from datetime import datetime, date
import uuid
from src.domain.aggregates.user import User
from src.domain.entities.identity import Identity
from src.domain.entities.document import Document
from src.domain.value_objects.address import Address
from src.domain.value_objects.birth_date import BirthDate
from src.domain.value_objects.wallet_address import WalletAddress
from src.domain.value_objects.risk_score import RiskScore
from src.domain.enums.kyc_level import KycLevel

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user_id = uuid.uuid4()
        self.identity = Identity(
            "John", 
            "Doe", 
            Address("123 Main St", "Anytown", "USA", "12345"),
            BirthDate(date(1990, 1, 1))
        )
        self.wallet_address = WalletAddress("0x1234567890123456789012345678901234567890")
        self.user = User(self.user_id, self.identity, self.wallet_address)

    def test_create_user(self):
        self.assertEqual(self.user.id, self.user_id)
        self.assertEqual(self.user.identity, self.identity)
        self.assertEqual(self.user.wallet_address, self.wallet_address)
        self.assertEqual(self.user.kyc_level, KycLevel.NONE)
        self.assertEqual(len(self.user.documents), 0)
        self.assertEqual(self.user.risk_score.score, 0)

    def test_add_document(self):
        document = Document(uuid.uuid4(), "Passport", "123456", datetime(2030, 1, 1))
        self.user.add_document(document)
        self.assertEqual(len(self.user.documents), 1)
        self.assertEqual(self.user.kyc_level, KycLevel.BASIC)

    def test_update_risk_score(self):
        self.user.update_risk_score(75)
        self.assertEqual(self.user.risk_score.score, 75)

    def test_kyc_level_update(self):
        for i in range(4):
            self.user.add_document(Document(uuid.uuid4(), f"Doc{i}", str(i), datetime(2030, 1, 1)))
        self.assertEqual(self.user.kyc_level, KycLevel.ADVANCED)

if __name__ == '__main__':
    unittest.main()