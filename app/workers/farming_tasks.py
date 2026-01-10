from celery import Celery
from app.core.config import settings
from app.domain.strategies.base_chain_strategy import BaseChainStrategy
from app.core.scheduler import Scheduler
from app.core.humanizer import Humanizer
from app.infrastructure.blockchain.web3_client import EVMClient
from app.infrastructure.blockchain.solana_client import SolanaClient
from app.infrastructure.database.db_manager import get_db_session
from app.infrastructure.database.models import Wallet, Task
from app.core.exceptions import TxFailedError
import requests
import time

app = Celery('tasks', broker=settings.REDIS_URL, backend=settings.REDIS_URL)

humanizer = Humanizer()
scheduler = Scheduler()

@app.task
def run_farming_task(wallet_id: int, strategy: str, user_chat_id: str):
    """Run farming task with full humanization and scheduler."""
    db = next(get_db_session())
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        return
    task = Task(wallet_id=wallet_id, status="running", type=strategy)
    db.add(task)
    db.commit()
    try:
        if strategy == "base":
            strat = BaseChainStrategy()
            client = EVMClient()
            tx = client.build_bridge_tx(wallet.address, 0.1)
            # Sign and send (assume private key from encrypted session; placeholder)
            # tx_hash = client.sign_and_send_tx(tx, decrypted_key)
            # For demo, simulate
            time.sleep(humanizer.random_delay(5, 15))
            task.status = "completed"
            # Update profit
            wallet.profit_estimate += client.get_profit_estimate("ethereum", 0.1)
        elif strategy == "solana":
            client = SolanaClient()
            # Similar for Solana
            pass
        # Notify via Telegram
        requests.post(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                      json={"chat_id": user_chat_id, "text": f"Task {strategy} completed for {wallet.address}"})
        # Schedule next farming and health
        scheduler.schedule_task(run_farming_task.apply_async, args=[wallet_id, strategy, user_chat_id], countdown=humanizer.calculate_sleep(3600))  # Hourly
        scheduler.schedule_task(run_health_task.apply_async, args=[wallet_id], countdown=humanizer.calculate_sleep(1440))  # Daily
    except Exception as e:
        task.status = "failed"
        raise TxFailedError("farming", str(e))
    finally:
        db.commit()

@app.task
def run_health_task(wallet_id: int):
    """Non-farming health task: e.g., periodic proxy ping or vote."""
    db = next(get_db_session())
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        return
    # Simulate health check: Ping proxy or vote on governance
    time.sleep(humanizer.random_delay(10, 30))
    # Placeholder: Implement real health logic, e.g., Snapshot vote via browser
    wallet.last_activity = time.time()
    db.commit()
    # Reschedule daily
    scheduler.schedule_task(run_health_task.apply_async, args=[wallet_id], countdown=humanizer.calculate_sleep(1440))
