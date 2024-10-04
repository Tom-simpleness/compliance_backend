# src/infrastructure/external_services/verify_id_service.py
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from src.domain.services.identity_verification_service import IIdentityVerificationService
from src.domain.entities.identity import Identity
import os
from cryptography.fernet import Fernet

class VerifyIDService(IIdentityVerificationService):
    def __init__(self):
        self.base_url = os.environ.get('VERIFY_ID_BASE_URL')
        self.api_key = self._decrypt_api_key()
        self.session = self._create_secure_session()

    def _decrypt_api_key(self):
        encrypted_key = os.environ.get('ENCRYPTED_VERIFY_ID_API_KEY')
        fernet_key = os.environ.get('FERNET_KEY')
        if not encrypted_key or not fernet_key:
            raise ValueError("Missing encryption keys in environment variables")
        f = Fernet(fernet_key.encode())
        return f.decrypt(encrypted_key.encode()).decode()

    def _create_secure_session(self):
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def verify_identity(self, identity: Identity) -> bool:
        url = f"{self.base_url}/verify"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ComplianceBackend/1.0"
        }
        payload = {
            "first_name": identity.first_name,
            "last_name": identity.last_name,
            "address": {
                "street": identity.address.street,
                "city": identity.address.city,
                "country": identity.address.country,
                "postal_code": identity.address.postal_code
            },
            "birth_date": str(identity.birth_date.value)
        }

        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result.get("verified", False)
        except requests.RequestException as e:
            # Log the error securely
            self._log_error(str(e))
            return False

    def _log_error(self, error_message: str):
        # Implement secure logging here
        # For example, use a secure logging service or write to a protected file
        pass