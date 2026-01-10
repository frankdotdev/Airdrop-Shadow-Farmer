# Frontend Build TODO

## Setup and Configuration
- [x] Install shadcn/ui components (Button, Card, Tabs, Slider, Switch)
- [x] Create .env.example file for secrets (API keys, etc.)
- [x] Configure Tailwind CSS for dark theme and custom styles
- [ ] Create frontend/.env with actual secrets

## Components Development
- [ ] Update Dashboard.tsx: Ensure shadcn components, add Profit Tracker with Coingecko, enhance activity feed
- [ ] Update Wallets.tsx: Add import form, Sybil scores display, integrate WalletConnect for connect/approve tx
- [ ] Create Strategies.tsx: Cards with sliders (aggression), toggles (Gas Guard), Airdrop Scanner integration
- [x] Create Profile.tsx: Subscriptions, referrals (generate code, track rewards)

## Integrations
- [ ] Integrate @twa-dev/sdk in AuthContext for Telegram user ID/theme
- [ ] Integrate WalletConnect v2 in useWalletConnect hook for non-custodial wallets
- [ ] Set up React Router in App.tsx for pages: /dashboard, /wallets, /strategies, /profile
- [ ] Add API hooks with axios for backend calls (add wallet, start farming, scan airdrops)

## Styling and UX
- [ ] Apply dark theme with Tailwind (rich gray bg, emerald/rose accents), monospaced addresses, micro-interactions (copy-to-clipboard checkmark, skeleton loaders)

## Testing and Deployment
- [ ] Add tests with Vitest for components/hooks
- [ ] Update docker-compose.yml for production (add Nginx reverse proxy)

## Additional Features
- [ ] Implement Airdrop Scanner: Backend /scan endpoint integration
- [ ] Profit Tracker: Coingecko API for farmed value estimation
- [ ] Referral System: Generate code, track rewards
