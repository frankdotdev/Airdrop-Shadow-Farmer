# Frontend Guide

This guide covers the React frontend of Shadow Farmer.

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Routing**: React Router v6
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: React Context (Auth), useState/useEffect
- **API**: Axios for HTTP calls
- **Web3**: @walletconnect/web3-provider for connections
- **Build**: Vite for fast dev/build
- **Icons**: Lucide React

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI
│   │   ├── ui/              # shadcn components (Button, Card, etc.)
│   │   ├── Dashboard.tsx    # Bento grid, activity feed
│   │   ├── Wallets.tsx      # Wallet list, import form
│   │   └── Strategies.tsx   # Strategy cards with sliders
│   ├── contexts/            # Global state
│   │   └── AuthContext.tsx  # TWA user, theme
│   ├── hooks/               # Custom hooks
│   │   └── useWalletConnect.tsx  # WC v2 integration
│   ├── pages/               # Route components
│   │   ├── Dashboard.tsx
│   │   ├── Wallets.tsx
│   │   ├── Strategies.tsx
│   │   └── Profile.tsx
│   ├── App.tsx              # Router setup
│   ├── main.tsx             # Entry point
│   └── index.css            # Tailwind imports
├── public/                  # Static assets
├── package.json             # Deps, scripts
└── vite.config.ts           # Build config
```

## Key Components

### Dashboard
- Bento grid layout (3x3 cards).
- Activity feed: Polls `/api/v1/tasks` every 5s.
- Profit chart: Recharts for USD estimates.
- Dark theme: Monospaced addresses, micro-interactions (copy with checkmark).

### Wallets
- List with Sybil scores (color-coded: green <20, yellow 20-50, red >50).
- Import form: WalletConnect QR scan.
- Actions: Edit proxy, delete.

### Strategies
- Cards for Bridge, Swap, Vote, Health.
- Sliders: Aggression (0-100), amount (ETH).
- Toggles: Gas Guard, notifications.
- Start button: Calls `/api/v1/farm/run`.

### AuthContext
- Integrates @twa-dev/sdk for Telegram user ID, theme.
- Stores JWT token.

### useWalletConnect
- Initializes WC v2 provider.
- Handles connect/disconnect, tx proposals.

## Development

### Setup
```bash
cd frontend
npm install --legacy-peer-deps
npm run dev  # http://localhost:3000
```

### Scripts
- `npm run build`: Production build
- `npm run preview`: Preview build
- `npm run lint`: ESLint
- `npm test`: Vitest (unit tests)

### Styling
- Tailwind: Utility classes (e.g., `bg-gray-900`, `text-emerald-500`).
- shadcn: Pre-built components (install: `npx shadcn-ui@latest add button`).
- Theme: Dark mode, Inter font, subtle borders.

### API Integration
- Axios instance in `src/api/client.ts`.
- Hooks: `useWallets()`, `useStrategies()` with SWR-like polling.
- Error handling: Toast notifications.

### Testing
- Vitest for components.
- Mock API responses.
- E2E: Playwright for full flows.

## Deployment

- Build: `npm run build`
- Serve: Nginx or Vercel.
- Env: VITE_API_URL for backend URL.

## Best Practices

- TypeScript strict.
- Responsive: Mobile-first.
- Accessibility: ARIA labels.
- Performance: Lazy load routes, memoize.

See README_FOR_DEVELOPERS.md for more.
