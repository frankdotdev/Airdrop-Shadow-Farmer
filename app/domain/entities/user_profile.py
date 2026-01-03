from typing import List
from pydantic import BaseModel

class UserProfile(BaseModel):
    telegram_id: str
    subscription_tier: str
    wallets: List[str]

class WalletEntity(BaseModel):
    address: str
    sybil_score: int
    proxy_ip: str