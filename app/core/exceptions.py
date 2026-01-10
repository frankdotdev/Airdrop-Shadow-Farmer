from fastapi import HTTPException
from typing import Optional

class ShadowFarmerException(Exception):
    """Base exception for Shadow Farmer."""
    def __init__(self, message: str, status_code: int = 500, detail: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(self.message)

class GasPriceTooHighError(ShadowFarmerException):
    """Raised when gas price exceeds threshold."""
    def __init__(self, current_gas: float, threshold: float):
        message = f"Gas price {current_gas} gwei exceeds threshold {threshold} gwei"
        super().__init__(message, status_code=429)

class CaptchaSolveError(ShadowFarmerException):
    """Raised when CAPTCHA solving fails."""
    def __init__(self, provider: str):
        message = f"Failed to solve CAPTCHA via {provider}"
        super().__init__(message, status_code=503)

class TxFailedError(ShadowFarmerException):
    """Raised when transaction fails."""
    def __init__(self, tx_hash: str, reason: str):
        message = f"Transaction {tx_hash} failed: {reason}"
        super().__init__(message, status_code=400)

class WalletConnectError(ShadowFarmerException):
    """Raised for WalletConnect issues."""
    def __init__(self, detail: str):
        message = f"WalletConnect error: {detail}"
        super().__init__(message, status_code=400)

class PaymentVerificationError(ShadowFarmerException):
    """Raised when USDT payment verification fails."""
    def __init__(self, tx_hash: str):
        message = f"Payment verification failed for tx {tx_hash}"
        super().__init__(message, status_code=400)

class AirdropScanError(ShadowFarmerException):
    """Raised when airdrop scanning fails."""
    def __init__(self, source: str):
        message = f"Airdrop scan failed from {source}"
        super().__init__(message, status_code=503)

class ReferralError(ShadowFarmerException):
    """Raised for referral issues."""
    def __init__(self, detail: str):
        message = f"Referral error: {detail}"
        super().__init__(message, status_code=400)

# Utility to raise HTTPException from custom exceptions
def raise_http_exception(exc: ShadowFarmerException):
    raise HTTPException(status_code=exc.status_code, detail=exc.detail)
