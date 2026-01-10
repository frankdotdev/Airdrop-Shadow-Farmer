# How Shadow Farmer Works

Shadow Farmer is a Telegram Mini App that automates airdrop farming across Web3 protocols while mimicking human behavior to avoid detection. It's non-custodial, using WalletConnect for secure interactions.

## Core Functionality

### 1. User Onboarding
- Users access via Telegram Mini App link.
- Authenticate with Telegram ID (no KYC).
- Generate unique referral code on signup.
- Select subscription tier: Hobbyist (free, limited), Whales ($10/month, unlimited), Protocol ($50/month, priority).

### 2. Wallet Management
- Add wallets via WalletConnect v2 (MetaMask, Trust, etc.).
- Encrypt session data with AES-256-GCM.
- Assign residential proxy per wallet (BrightData).
- Calculate Sybil score (0-100) based on on-chain activity.

### 3. Farming Automation
- Select strategies: Bridge (Base), Swap (Uniswap/Jupiter), Vote (governance), Health (check balances).
- Humanizer adds random delays (1-5s), jitters, mouse movements.
- Gas Guard: Monitor gas prices, retry if >50 gwei, use EIP-1559.
- Slippage protection: Max 0.5% slippage.
- Execute via stealth browser: Playwright with stealth plugin, proxy rotation, fingerprint spoofing.

### 4. Airdrop Scanning
- Poll Coingecko API for new projects.
- Scrape Twitter (via requests) for airdrop announcements.
- Filter by chain, volume, community size.
- Notify users via Telegram bot.

### 5. Profit Tracking
- Estimate farmed value using Coingecko prices.
- Track in DB, display in Dashboard.
- Referral rewards: 10% commission on referred users' profits.

### 6. Payment & Subscriptions
- USDT payments verified on-chain.
- Web3 verification: Check tx hash for subscription.
- Tiers unlock features: More wallets, faster farming, priority support.

## Technical Flow

1. User clicks "Start Farming" in TWA.
2. Frontend sends request to FastAPI backend.
3. Backend validates JWT, queues Celery task.
4. Worker picks task: Initializes stealth browser, connects wallet, executes strategy.
5. Browser solves CAPTCHA via CapSolver if needed.
6. Signs tx via WalletConnect, submits to RPC.
7. Monitors confirmation, updates DB.
8. Notifies user via Telegram.

## Anti-Detection Measures
- Randomized actions: Delays, paths, timings.
- Proxy rotation: New IP per session.
- Fingerprint spoofing: Vary user agent, screen size.
- Low-volume farming: Avoid rate limits.

## Scalability
- Async tasks via Celery + Redis.
- Horizontal scaling: Multiple workers.
- Caching: Redis for prices, sessions.

## Security
- Non-custodial: Keys stay in user's wallet.
- Encrypted DB: Sensitive fields AES-encrypted.
- HTTPS everywhere, JWT auth.

The app farms airdrops ethically, focusing on small, emerging projects to build community.
