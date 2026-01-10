from app.infrastructure.database.db_manager import get_db_session
from app.infrastructure.database.models import User, Wallet
from app.core.security import SecurityLayer
import uuid

def seed_data():
    """Seed initial data for development."""
    db = next(get_db_session())
    security = SecurityLayer()

    # Seed admin user
    admin = User(
        id=uuid.uuid4(),
        telegram_id="123456789",
        subscription_tier="protocol",
        referral_code="ADMIN123"
    )
    db.add(admin)

    # Seed sample wallet
    wallet = Wallet(
        address="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        encrypted_session=security.encrypt_session("sample_session"),
        proxy_ip="127.0.0.1",
        user_id=admin.id,
        sybil_score=0.1,
        profit_estimate=100.0
    )
    db.add(wallet)

    db.commit()
    print("Seeded data successfully.")

if __name__ == "__main__":
    seed_data()
