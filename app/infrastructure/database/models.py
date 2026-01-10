from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    subscription_tier = Column(String, default="hobbyist")  # hobbyist, whales, protocol
    referral_code = Column(String, unique=True, index=True)  # For referral system
    referred_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Self-referencing for referrals
    created_at = Column(DateTime, default=datetime.utcnow)
    wallets = relationship("Wallet", back_populates="user")
    referrals = relationship("User", backref="referrer", remote_side=[id])

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String, unique=True)
    encrypted_session = Column(Text)  # Encrypted WalletConnect session
    proxy_ip = Column(String)  # Assigned residential proxy
    sybil_score = Column(Integer, default=0)  # 0-100
    profit_estimate = Column(Float, default=0.0)  # Estimated farmed value in USD
    last_activity = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="wallets")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    status = Column(String)  # pending, running, completed, failed
    type = Column(String)  # bridge, swap, vote, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
