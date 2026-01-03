from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    subscription_tier = Column(String, default="hobbyist")  # hobbyist, whales, protocol
    wallets = relationship("Wallet", back_populates="user")

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String, unique=True)
    encrypted_session = Column(Text)  # Encrypted WalletConnect session
    proxy_ip = Column(String)  # Assigned residential proxy
    sybil_score = Column(Integer, default=0)  # 0-100
    user = relationship("User", back_populates="wallets")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    status = Column(String)  # pending, running, completed
    type = Column(String)  # bridge, swap, etc.