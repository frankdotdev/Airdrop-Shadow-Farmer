import random
import time
from zoneinfo import ZoneInfo  # Python 3.12 feature for timezones

class Humanizer:
    def calculate_sleep(self, base_minutes: int = 60) -> float:
        jitter = base_minutes * 0.2
        sleep_time = random.uniform(base_minutes - jitter, base_minutes + jitter)
        return sleep_time * 60

    def randomize_amount(self, amount: float) -> float:
        variation = random.uniform(0.98, 1.02)
        return round(amount * variation, 5)

    def is_working_hours(self, timezone: str = "UTC") -> bool:
        current_time = time.localtime(time.time())
        hour = current_time.tm_hour
        return 8 <= hour <= 22  # Daytime to avoid night farming detection