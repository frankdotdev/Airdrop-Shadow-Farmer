from web3 import Web3
from app.core.config import settings
from app.core.humanizer import Humanizer

class EVMClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.ALCHEMY_RPC_URL))
        self.humanizer = Humanizer()

    def build_bridge_tx(self, user_address: str, amount_eth: float, bridge_contract_address: str, abi: list) -> dict:
        amount = self.humanizer.randomize_amount(amount_eth)
        contract = self.w3.eth.contract(address=bridge_contract_address, abi=abi)
        tx = contract.functions.depositETH().build_transaction({
            'from': user_address,
            'value': self.w3.to_wei(amount, 'ether'),
            'nonce': self.w3.eth.get_transaction_count(user_address),
            'gas': 150000,
            'maxFeePerGas': self.w3.eth.max_priority_fee + self.w3.eth.gas_price,
            'chainId': self.w3.eth.chain_id
        })
        return tx

    def check_gas(self) -> bool:
        gas_price = self.w3.eth.gas_price / 10**9  # gwei
        return gas_price < 20  # Gas Guard