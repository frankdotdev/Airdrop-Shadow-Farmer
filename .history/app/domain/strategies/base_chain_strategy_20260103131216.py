from app.infrastructure.blockchain.web3_client import EVMClient
from app.core.humanizer import Humanizer

class GasPriceTooHighError(Exception):
    pass

class BaseChainStrategy:
    def __init__(self):
        self.client = EVMClient()
        self.humanizer = Humanizer()

    async def execute_bridge(self, user_address: str, amount: float, bridge_contract_address: str = "0x3154Cf16ccdb4C6d922629664174b904d80F2C35", abi: list = []):
        if not self.client.check_gas():
            raise GasPriceTooHighError("Gas too high")
        tx = self.client.build_bridge_tx(user_address, amount, bridge_contract_address, abi)
        return tx  # Send to user for signing

    def calculate_sybil_score(self, address: str) -> int:
        tx_count = self.client.w3.eth.get_transaction_count(address)
        # Simple heuristic: Low tx = new = high sybil risk
        score = min(100, 100 - tx_count * 2)  # Advanced: Use graph analysis API
        return score
