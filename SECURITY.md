# Security Overview

Shadow Farmer prioritizes security for non-custodial operations.

## Encryption

- AES-256-GCM for session data (cryptography library).
- JWT for API auth (python-jose).
- Encrypted DB fields for sensitive info.

## Anti-Detection

- Residential proxies (BrightData).
- Fingerprint spoofing (playwright-stealth).
- Humanized delays (random 1-5s).
- CAPTCHA solving (CapSolver).

## Access Control

- JWT tokens with 30min expiry.
- Role-based: user, admin.
- Rate limiting (FastAPI middleware).

## Blockchain Security

- Gas Guard: Max 50 gwei, retries.
- Slippage protection: 0.5% max.
- Non-custodial: User signs txs.

## Infrastructure

- Secrets in .env, not code.
- HTTPS everywhere.
- Audit logs.

## Vulnerabilities

- Report to security@shadowfarmer.com.
- No bounties yet.

## Compliance

- GDPR: Data minimization.
- No KYC for privacy.

## Best Practices

- Rotate keys quarterly.
- Monitor for anomalies.
- Use VPN for development.
