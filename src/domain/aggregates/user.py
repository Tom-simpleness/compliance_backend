# src/domain/aggregates/user.py
from dataclasses import dataclass, field
from ..entities.identity import Identity
from ..entities.document import Document
from ..value_objects.wallet_address import WalletAddress
from ..value_objects.risk_score import RiskScore
from ..enums.kyc_level import KycLevel
import uuid

@dataclass
class User:
    id: uuid.UUID
    identity: Identity
    wallet_address: WalletAddress
    kyc_level: KycLevel = KycLevel.NONE
    risk_score: RiskScore = field(default_factory=lambda: RiskScore(0))
    documents: list[Document] = field(default_factory=list)

    def add_document(self, document: Document):
        self.documents.append(document)
        self._update_kyc_level()

    def update_risk_score(self, score: int):
        self.risk_score = RiskScore(score)

    def _update_kyc_level(self):
        self.kyc_level = KycLevel(min(len(self.documents), KycLevel.ADVANCED.value))