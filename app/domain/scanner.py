import requests
from app.core.config import settings
from typing import List, Dict

class AirdropScanner:
    def scan_coingecko(self) -> List[Dict]:
        """Scan Coingecko for new projects (airdrop candidates)."""
        url = "https://api.coingecko.com/api/v3/coins/list"
        headers = {"Authorization": f"Bearer {settings.COINGECKO_API_KEY}"} if settings.COINGECKO_API_KEY else {}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            coins = response.json()
            # Filter for new coins (low market cap, recent launch)
            new_projects = [coin for coin in coins if coin.get("market_cap_rank", 1000) > 500 and coin.get("id") not in ["bitcoin", "ethereum"]]  # Exclude majors
            return new_projects[:10]  # Limit to 10
        return []

    def scan_twitter(self, keywords: List[str] = ["airdrop", "testnet", "farm"]) -> List[Dict]:
        """Scan Twitter for airdrop mentions using Twitter API v2."""
        # Use Twitter API v2 (requires Bearer token)
        bearer_token = settings.TWITTER_BEARER_TOKEN
        if not bearer_token:
            return []
        headers = {"Authorization": f"Bearer {bearer_token}"}
        query = " OR ".join(keywords)
        url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=10"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return [{"text": tweet["text"], "url": f"https://twitter.com/i/web/status/{tweet['id']}"} for tweet in data.get("data", [])]
        return []
