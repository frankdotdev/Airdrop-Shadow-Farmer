from cryptography.fernet import Fernet
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.exceptions import raise_http_exception

class SecurityLayer:
    def __init__(self):
        self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())
        self.secret_key = settings.ENCRYPTION_KEY  # Reuse for JWT
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def encrypt_session(self, session_data: str) -> bytes:
        """AES-256-GCM encryption for sessions."""
        return self.cipher.encrypt(session_data.encode())

    def decrypt_session(self, encrypted_data: bytes) -> str:
        """Decrypt sessions."""
        return self.cipher.decrypt(encrypted_data).decode()

    def create_access_token(self, data: dict):
        """Create JWT token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str):
        """Verify JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
