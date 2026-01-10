from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.workers.farming_tasks import run_farming_task, check_sybil_score
from app.infrastructure.database.db_manager import get_db
from app.infrastructure.database.models import User, Wallet
from app.core.config import settings
from web3 import Web3

router = APIRouter()

@router.post("/start")
def start_farming(strategy: str, wallet_id: int, user_chat_id: str, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    run_farming_task.delay(wallet_id, strategy, user_chat_id)
    return {"status": "scheduled"}

@router.get("/status/{user_id}")
def get_status(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    wallets = db.query(Wallet).filter(Wallet.user_id == user_id).all()
    return {"user": user.telegram_id, "tier": user.subscription_tier, "wallets": [{"address": w.address, "sybil_score": w.sybil_score} for w in wallets]}

@router.post("/sybil_check/{wallet_id}")
def sybil_check(wallet_id: int):
    check_sybil_score.delay(wallet_id)
    return {"status": "checking"}

@router.post("/subscribe")
def subscribe(tier: str, payment_tx: str, user_id: int, db: Session = Depends(get_db)):
    # Verify USDT tx on TRON/BSC using web3
    w3_tron = Web3(Web3.HTTPProvider("https://api.trongrid.io"))  # Example for TRON
    # Add verification logic here
    user = db.query(User).filter(User.id == user_id).first()
    user.subscription_tier = tier
    db.commit()
    return {"status": "subscribed"}

@router.get("/analytics/{user_id}")
def get_analytics(user_id: int, db: Session = Depends(get_db)):
    wallets = db.query(Wallet).filter(Wallet.user_id == user_id).all()
    total_value = sum(w.sybil_score for w in wallets)  # Placeholder for actual value
    return {"total_estimated_value": total_value}
