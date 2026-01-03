import random

class FingerprintGenerator:
    def generate(self) -> dict:
        user_agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",  # Mac
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"]  # Windows
        return {"user_agent": random.choice(user_agents), "viewport": {"width": random.randint(1280, 1920), "height": random.randint(720, 1080)}}