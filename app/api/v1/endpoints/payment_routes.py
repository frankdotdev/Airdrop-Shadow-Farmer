from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.db_manager import get_db
from app.infrastructure.database.models import User
from app.infrastructure.blockchain.web3_client import EVMClient
from app.core.config import settings
from app.core.exceptions import PaymentVerificationError
from web3 import Web3

router = APIRouter()

PLATFORM_ADDRESS = "0xYourPlatformAddress"  # Replace with actual USDT contract or platform wallet
USDT_CONTRACT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT on Ethereum
TIER_PRICES = {"hobbyist": 10, "whales": 50, "protocol": 100}  # USDT amounts

@router.post("/subscribe")
def subscribe(user_id: int, tier: str, tx_hash: str, db: Session = Depends(get_db)):
    """Verify USDT payment and update subscription."""
    if tier not in TIER_PRICES:
        raise HTTPException(status_code=400, detail="Invalid tier")
    required_amount = TIER_PRICES[tier]
    try:
        client = EVMClient()
        w3 = Web3(Web3.HTTPProvider(settings.ALCHEMY_RPC_URL))
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        if not receipt or receipt.status != 1:
            raise PaymentVerificationError(tx_hash)
        # Check if tx is to platform and amount >= required
        tx = w3.eth.get_transaction(tx_hash)
        if tx.to != PLATFORM_ADDRESS:
            raise PaymentVerificationError(tx_hash)
        # For USDT transfer, decode logs (simplified; use contract events)
        # Assuming direct ETH or USDT; in prod, check ERC20 transfer event
        amount_received = w3.from_wei(tx.value, 'ether') if tx.value else 0  # Placeholder for USDT
        if amount_received < required_amount:
            raise PaymentVerificationError(tx_hash)
        # Update user tier
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.subscription_tier = tier
        db.commit()
        return {"status": "subscribed", "tier": tier}
    except Exception as e:
        raise PaymentVerificationError(tx_hash)
