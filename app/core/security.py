from cryptography.fernet import Fernet
from app.core.config import settings

class SecurityLayer:
    def __init__(self):
        self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())

    def encrypt_session(self, session_data: str) -> bytes:
        return self.cipher.encrypt(session_data.encode())

    def decrypt_session(self, encrypted_data: bytes) -> str:
        return self.cipher.decrypt(encrypted_data).decode()