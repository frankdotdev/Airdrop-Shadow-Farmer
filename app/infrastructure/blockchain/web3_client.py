import requests
import time
from web3 import Web3
from app.core.config import settings
from app.core.humanizer import Humanizer
from app.core.exceptions import GasPriceTooHighError, TxFailedError
import redis

# Real ABI for Base Bridge depositETH (from Etherscan)
BRIDGE_ABI = [
    {
        "inputs": [],
        "name": "depositETH",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

# Real ABI for Uniswap V3 Router swapExactETHForTokens (from Etherscan)
SWAP_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactETHForTokens",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "payable",
        "type": "function"
    }
]

class EVMClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.ALCHEMY_RPC_URL))
        self.humanizer = Humanizer()
        self.redis = redis.from_url(settings.REDIS_URL)
        self.gas_threshold_gwei = 50  # Dynamic Gas Guard max
        self.slippage_bps = 50  # 0.5% slippage
        self.max_retries = 3

    def build_bridge_tx(self, user_address: str, amount_eth: float, bridge_contract_address: str = "0x49048044D57e1C92A77f79988d21Fa8fAF74E97e") -> dict:  # Base Bridge
        amount = self.humanizer.randomize_amount(amount_eth)
        contract = self.w3.eth.contract(address=bridge_contract_address, abi=BRIDGE_ABI)
        nonce = self.w3.eth.get_transaction_count(user_address)
        gas_price = self._get_dynamic_gas_price()
        tx = contract.functions.depositETH().build_transaction({
            'from': user_address,
            'value': self.w3.to_wei(amount, 'ether'),
            'nonce': nonce,
            'gas': 150000,
            'maxFeePerGas': gas_price,
            'maxPriorityFeePerGas': self.w3.eth.max_priority_fee,
            'chainId': self.w3.eth.chain_id
        })
        return tx

    def build_swap_tx(self, user_address: str, amount_eth: float, token_out: str, router_address: str = "0xE592427A0AEce92De3Edee1F18E0157C05861564") -> dict:  # Uniswap V3 Router
        amount = self.humanizer.randomize_amount(amount_eth)
        contract = self.w3.eth.contract(address=router_address, abi=SWAP_ABI)
        path = [self.w3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"), self.w3.to_checksum_address(token_out)]  # WETH -> Token
        amount_out_min = self._calculate_min_out(amount, token_out) * (1 - self.slippage_bps / 10000)
        deadline = int(time.time()) + 300  # 5 min
        nonce = self.w3.eth.get_transaction_count(user_address)
        gas_price = self._get_dynamic_gas_price()
        tx = contract.functions.swapExactETHForTokens(
            int(amount_out_min), path, user_address, deadline
        ).build_transaction({
            'from': user_address,
            'value': self.w3.to_wei(amount, 'ether'),
            'nonce': nonce,
            'gas': 200000,
            'maxFeePerGas': gas_price,
            'maxPriorityFeePerGas': self.w3.eth.max_priority_fee,
            'chainId': self.w3.eth.chain_id
        })
        return tx

    def _get_dynamic_gas_price(self) -> int:
        """Get dynamic gas price with Gas Guard."""
        gas_price = self.w3.eth.gas_price / 10**9  # gwei
        if gas_price > self.gas_threshold_gwei:
            raise GasPriceTooHighError(gas_price, self.gas_threshold_gwei)
        return self.w3.to_wei(gas_price, 'gwei')

    def _calculate_min_out(self, amount_eth: float, token_out: str) -> float:
        """Calculate min out amount using cached price."""
        price = self.get_profit_estimate(token_out, 1)  # Price per token
        return amount_eth * price if price else 0

    def sign_and_send_tx(self, tx: dict, private_key: str) -> str:
        """Sign and send tx with retries."""
        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        for attempt in range(self.max_retries):
            try:
                tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                if receipt.status == 1:
                    return tx_hash.hex()
                else:
                    raise TxFailedError(tx_hash.hex(), "Transaction reverted")
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise TxFailedError("unknown", str(e))
                time.sleep(2 ** attempt)  # Exponential backoff

    def get_profit_estimate(self, token_symbol: str, amount: float) -> float:
        """Estimate profit using cached Coingecko API."""
        cache_key = f"coingecko:{token_symbol.lower()}"
        cached = self.redis.get(cache_key)
        if cached:
            price = float(cached)
        else:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_symbol.lower()}&vs_currencies=usd"
            headers = {"Authorization": f"Bearer {settings.COINGECKO_API_KEY}"} if settings.COINGECKO_API_KEY else {}
            response = requests.get(url, headers=headers, timeout=10)
            price = response.json().get(token_symbol.lower(), {}).get("usd", 0) if response.status_code == 200 else 0
            self.redis.setex(cache_key, 300, price)  # Cache 5 min
        return amount * price
