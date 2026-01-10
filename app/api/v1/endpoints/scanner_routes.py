from fastapi import APIRouter
from app.domain.scanner import AirdropScanner
from app.core.exceptions import AirdropScanError

router = APIRouter()

@router.get("/scan")
def scan_airdrops():
    """Scan for new airdrop opportunities."""
    try:
        scanner = AirdropScanner()
        coingecko_results = scanner.scan_coingecko()
        twitter_results = scanner.scan_twitter()
        opportunities = coingecko_results + [{"source": "twitter", **tweet} for tweet in twitter_results]
        return {"opportunities": opportunities}
    except Exception as e:
        raise AirdropScanError("general")
