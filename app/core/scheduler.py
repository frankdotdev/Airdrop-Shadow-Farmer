import asyncio
from app.core.humanizer import Humanizer

humanizer = Humanizer()

async def schedule_task(task_func, *args):
    delay = humanizer.calculate_sleep(5)  # Random delay
    await asyncio.sleep(delay)
    await task_func(*args)