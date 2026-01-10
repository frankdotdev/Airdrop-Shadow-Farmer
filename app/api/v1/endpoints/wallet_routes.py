from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.db_manager import get_db
from app.infrastructure.database.models import Wallet, User
from app.core.security import SecurityLayer
from app.stealth.fingerprints import FingerprintGenerator
from app.core.config import settings
from app.core.exceptions import WalletConnectError
from walletconnect import WalletConnect
import requests
import uuid

router = APIRouter()

@router.post("/add")
def add_wallet(address: str, session_data: str, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    security = SecurityLayer()
    encrypted = security.encrypt_session(session_data)
    proxy = settings.BRIGHTDATA_PROXY_URL  # Assign proxy
    fp_gen = FingerprintGenerator()
    fp = fp_gen.generate()
    wallet = Wallet(address=address, encrypted_session=encrypted, proxy_ip=proxy, user_id=user_id)
    db.add(wallet)
    db.commit()
    return {"status": "added", "wallet_id": wallet.id}

@router.get("/list/{user_id}")
def list_wallets(user_id: int, db: Session = Depends(get_db)):
    wallets = db.query(Wallet).filter(Wallet.user_id == user_id).all()
    return [{"id": w.id, "address": w.address, "sybil_score": w.sybil_score, "profit_estimate": w.profit_estimate} for w in wallets]

@router.delete("/remove/{wallet_id}")
def remove_wallet(wallet_id: int, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    db.delete(wallet)
    db.commit()
    return {"status": "removed"}

@router.post("/walletconnect/init")
def init_walletconnect(user_id: int, db: Session = Depends(get_db)):
    """Generate WalletConnect URI and store session."""
    try:
        wc = WalletConnect(project_id=settings.WALLET_CONNECT_PROJECT_ID)
        uri = wc.generate_uri()
        session_topic = str(uuid.uuid4())
        # Store encrypted session topic in DB (placeholder; in prod, store full session)
        security = SecurityLayer()
        encrypted_topic = security.encrypt_session(session_topic)
        # Update user or wallet with encrypted_topic (assume user for simplicity)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # For demo, store in a new field; in prod, add to models
        return {"uri": uri, "session_topic": session_topic}
    except Exception as e:
        raise WalletConnectError(str(e))

@router.post("/walletconnect/approve")
def approve_walletconnect_proposal(session_topic: str, approved: bool, db: Session = Depends(get_db)):
    """Approve or reject WalletConnect proposal."""
    try:
        wc = WalletConnect(project_id=settings.WALLET_CONNECT_PROJECT_ID)
        if approved:
            # Approve and store session
            security = SecurityLayer()
            encrypted = security.encrypt_session(session_topic)
            # Store in wallet (find by user; placeholder)
            return {"status": "approved", "session": encrypted.decode()}
        else:
            return {"status": "rejected"}
    except Exception as e:
        raise WalletConnectError(str(e))
