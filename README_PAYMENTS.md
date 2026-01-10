# Payments Guide

This guide covers payment handling in Shadow Farmer, including subscriptions and USDT verification.

## Subscription Tiers

- **Hobbyist**: Free, 1 wallet, 10 farms/month.
- **Whales**: $10/month, unlimited wallets, advanced strategies.
- **Protocol**: $50/month, priority farming, custom support.

## Payment Flow

1. User selects tier in Profile page.
2. App generates USDT payment address (Ethereum network).
3. User sends exact amount (e.g., 10 USDT for Whales).
4. App polls blockchain for confirmation (via web3_client).
5. On success: Updates DB, unlocks features, sends Telegram notification.

## Technical Implementation

### Backend
- Endpoint: `POST /api/v1/payment/subscribe`
  - Body: `{tier: "whales", amount: 10}`
  - Returns: `{address: "0x...", tx_hash: null}`
- Verification: `web3_client.verify_usdt_payment(tx_hash, amount, user_wallet)`
  - Checks ERC-20 transfer to app wallet.
  - Confirms amount, sender.

### Frontend
- Payment modal: Displays QR code, address.
- Polls `/api/v1/payment/status/{tx_hash}` every 10s.
- Success: Toast "Subscription activated!"

## Security
- No custodial funds: Payments to app-controlled wallet.
- Verification on-chain: Prevents fake claims.
- Refunds: Manual via support (rare).

## Integrations
- USDT on Ethereum (Tether contract: 0xdAC17F958D2ee523a2206206994597C13D831ec7).
- Future: Multi-currency (ETH, SOL).

## Troubleshooting
- Tx not confirming: Check gas, network congestion.
- Wrong amount: Refund via email.
- Disputes: Blockchain proof.

## Revenue Tracking
- DB: `payments` table (user_id, amount, tx_hash, date).
- Analytics: Monthly revenue, churn.

For pricing details, see README_PRICING.md.
