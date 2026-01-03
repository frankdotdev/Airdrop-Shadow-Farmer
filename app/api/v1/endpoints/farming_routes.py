from fastapi import APIRouter, Depends
from app.workers.farming_tasks import run_farming_task

router = APIRouter()

@router.post("/start")
def start_farming(strategy: str, wallet_id: int):
    run_farming_task.delay(wallet_id, strategy)
    return {"status": "scheduled"}