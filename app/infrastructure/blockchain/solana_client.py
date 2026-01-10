import time
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.publickey import PublicKey
from solana.keypair import Keypair
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import transfer_checked, TransferCheckedParams
from app.core.config import settings
from app.core.humanizer import Humanizer
from app.core.exceptions import TxFailedError
import redis

# Jupiter Swap Program ID (real from Solana explorer)
JUPITER_PROGRAM_ID = PublicKey("JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4")

# Simplified Jupiter Swap Instruction (route from Jupiter API)
# Note: Full Jupiter integration requires API for routes; this is a basic transfer fallback
class SolanaClient:
    def __init__(self):
        self.client = Client(settings.INFURA_RPC_URL or "https://api.mainnet.solana.com")  # Use Infura if set
        self.humanizer = Humanizer()
        self.redis = redis.from_url(settings.REDIS_URL)
        self.priority_fee_lamports = 5000  # Base priority fee
        self.slippage_bps = 50  # 0.5% slippage in basis points

    def build_swap_tx(self, user_pubkey: str, token_in: str, token_out: str, amount: float, jupiter_route: dict = None) -> Transaction:
        """Build a swap transaction using Jupiter or fallback to simple transfer."""
        amount = self.humanizer.randomize_amount(amount)
        user_key = PublicKey(user_pubkey)
        tx = Transaction()

        if jupiter_route:
            # Use Jupiter route (assumed from API call)
            # Add Jupiter instruction (simplified; real impl needs Jupiter SDK)
            # For production, integrate @jup-ag/api or similar
            pass  # Placeholder for full Jupiter logic
        else:
            # Fallback: Simple SOL transfer (for testing; replace with real swap)
            recipient = PublicKey("So11111111111111111111111111111111111111112")  # WSOL mint as example
            params = TransferParams(from_pubkey=user_key, to_pubkey=recipient, lamports=int(amount * 10**9))  # Assume SOL
            tx.add(transfer(params))

        # Add priority fee
        recent_blockhash = self.client.get_recent_blockhash()['result']['value']['blockhash']
        tx.recent_blockhash = recent_blockhash
        tx.fee_payer = user_key
        # Simulate priority fee addition (Solana has compute budget program)
        return tx

    def get_priority_fee(self) -> int:
        """Get dynamic priority fee from recent fees."""
        try:
            fees = self.client.get_recent_prioritization_fees()
            avg_fee = sum(fee['prioritizationFee'] for fee in fees) / len(fees) if fees else self.priority_fee_lamports
            return max(avg_fee, self.priority_fee_lamports)
        except:
            return self.priority_fee_lamports

    def sign_and_send_tx(self, tx: Transaction, keypair: Keypair) -> str:
        """Sign and send transaction, wait for confirmation."""
        tx.sign(keypair)
        tx_hash = self.client.send_transaction(tx, keypair)['result']
        # Wait for confirmation
        for _ in range(30):  # Up to 30s
            status = self.client.get_transaction(tx_hash)
            if status['result'] and status['result']['meta']['err'] is None:
                return tx_hash
            time.sleep(1)
        raise TxFailedError(tx_hash, "Transaction failed or timed out")

    def get_profit_estimate(self, token_symbol: str, amount: float) -> float:
        """Estimate profit using cached Coingecko (reuse logic from EVMClient)."""
        # For simplicity, assume same as EVM; in prod, use Solana-specific oracles
        cache_key = f"coingecko:{token_symbol.lower()}"
        cached = self.redis.get(cache_key)
        if cached:
            price = float(cached)
        else:
            # Call Coingecko (same as EVM)
            import requests
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_symbol.lower()}&vs_currencies=usd"
            headers = {"Authorization": f"Bearer {settings.COINGECKO_API_KEY}"} if settings.COINGECKO_API_KEY else {}
            response = requests.get(url, headers=headers, timeout=10)
            price = response.json().get(token_symbol.lower(), {}).get("usd", 0) if response.status_code == 200 else 0
            self.redis.setex(cache_key, 300, price)
        return amount * price
