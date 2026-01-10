from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.db_manager import get_db
from app.infrastructure.database.models import Wallet
from app.core.security import SecurityLayer
from app.stealth.fingerprints import FingerprintGenerator

router = APIRouter()

@router.post("/add")
def add_wallet(address: str, session_data: str, db: Session = Depends(get_db)):
    security = SecurityLayer()
    encrypted = security.encrypt_session(session_data)
    proxy = "assigned_proxy"  # From BrightData
    fp_gen = FingerprintGenerator()
    fp = fp_gen.generate()
    wallet = Wallet(address=address, encrypted_session=encrypted, proxy_ip=proxy)
    db.add(wallet)
    db.commit()
    return {"status": "added"}