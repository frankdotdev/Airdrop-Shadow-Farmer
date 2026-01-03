from solana.rpc.api import Client
from solana.transaction import Transaction
from app.core.config import settings
from app.core.humanizer import Humanizer

class SolanaClient:
    def __init__(self):
        self.client = Client("https://api.mainnet.solana.com")  # Or your RPC
        self.humanizer = Humanizer()

    def build_swap_tx(self, user_pubkey: str, amount: float) -> Transaction:
        # Example: Build a simple transfer tx (expand for swaps)
        amount = self.humanizer.randomize_amount(amount)
        tx = Transaction()
        # Add instructions here (e.g., for Jupiter swap)
        return tx