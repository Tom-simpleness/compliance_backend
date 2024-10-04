# src/domain/aggregates/user.py
from dataclasses import dataclass, field
from ..entities.identity import Identity
from ..entities.document import Document
from ..value_objects.wallet_address import WalletAddress
from ..value_objects.risk_score import RiskScore
from ..enums.kyc_level import KycLevel
from uuid import UUID

@dataclass
class User:
    id: UUID
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
        document_count = len(self.documents)
        if self.kyc_level == KycLevel.NONE or self.kyc_level == KycLevel.FAILED:
            if document_count == 1:
                self.kyc_level = KycLevel.BASIC
            elif document_count == 2:
                self.kyc_level = KycLevel.INTERMEDIATE
            elif document_count >= 3:
                self.kyc_level = KycLevel.ADVANCED
        elif self.kyc_level == KycLevel.BASIC and document_count >= 2:
            self.kyc_level = KycLevel.INTERMEDIATE
        elif self.kyc_level == KycLevel.INTERMEDIATE and document_count >= 3:
            self.kyc_level = KycLevel.ADVANCED

    def update_kyc_level(self, level: KycLevel):
        self.kyc_level = level