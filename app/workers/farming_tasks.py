from celery import Celery
from app.core.config import settings
from app.domain.strategies.base_chain_strategy import BaseChainStrategy

app = Celery('tasks', broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@app.task
def run_farming_task(wallet_id: int, strategy: str):
    if strategy == "base":
        strat = BaseChainStrategy()
        tx = strat.execute_bridge("user_address", 0.1)  # Get from DB
        # Send notification via Telegram API
        requests.post(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage", json={"chat_id": "user_chat_id", "text": f"Sign this tx: {tx}"})