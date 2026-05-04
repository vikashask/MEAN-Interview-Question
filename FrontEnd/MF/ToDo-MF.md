ToDo

## Proposed Architecture

### 1 Architecture Pattern

**Chosen**: Module Federation (Webpack 5)

**Why**:

- ✅ Runtime integration (no build coupling)
- ✅ Shared dependencies (React, MUI, Apollo)
- ✅ Dynamic remote loading
- ✅ Production-ready, React 18+ compatible

### 2 High-Level Architecture

```
┌───────────────────────────────────────────────────────┐
│              Shell Application (Host)                  │
│  - Authentication (Okta)                              │
│  - Global Layout (Header, Sidebar)                    │
│  - Top-level Routing                                  │
│  - Shared Contexts (Auth, Config, Apollo)            │
└───────────────────────────────────────────────────────┘
         ↓ Lazy loads via Module Federation
┌─────────┬─────────┬─────────┬─────────┬─────────────┐
│MFE      │MFE      │MFE      │MFE      │MFE          │
│Campaigns│Rewards  │Members  │Content  │Sweepstakes  │
└─────────┴─────────┴─────────┴─────────┴─────────────┘
┌─────────┬─────────┬─────────┬─────────────────────────┐
│MFE      │MFE      │MFE      │MFE                      │
│Support  │Mgmt     │Partners │Dashboard                │
└─────────┴─────────┴─────────┴─────────────────────────┘
         ↓ Shared via Module Federation
┌──────────────┬──────────────┬──────────────┬──────────┐
│Shared UI     │Shared Utils  │Shared Types  │Shared    │
│(Components)  │(Functions)   │(TypeScript)  │GraphQL   │
└──────────────┴──────────────┴──────────────┴──────────┘
```

### 3 Package Structure

```
loyalty-admin-ui/
├── packages/
│   ├── shell/                    # Host Application
│   ├── mfe-campaigns/            # Campaigns MFE
│   ├── mfe-rewards/              # Rewards MFE
│   ├── mfe-members/              # Members MFE
│   ├── mfe-content/              # Content/Banners/Surveys MFE
│   ├── mfe-sweepstakes/          # Sweepstakes MFE
│   ├── mfe-customer-support/     # Support MFE
│   ├── mfe-management/           # Settings MFE
│   ├── mfe-partners/             # Partners/Segments MFE
│   ├── mfe-dashboard/            # Dashboard/Analytics MFE
│   ├── shared-ui/                # Component Library
│   ├── shared-utils/             # Utilities
│   ├── shared-types/             # TypeScript Types
│   └── shared-graphql/           # GraphQL Layer
└── tools/                        # Build Tools
```

---

## Technical Implementation

### 4.1 Module Federation Config

**Shell webpack.config.js**:

```javascript
new ModuleFederationPlugin({
  name: "shell",
  remotes: {
    mfe_campaigns: "mfe_campaigns@[url]/remoteEntry.js",
    mfe_rewards: "mfe_rewards@[url]/remoteEntry.js",
    // ... other remotes
  },
  shared: {
    react: { singleton: true, eager: true },
    "react-dom": { singleton: true, eager: true },
    "react-router-dom": { singleton: true },
    "@mui/material": { singleton: true },
    "@apollo/client": { singleton: true },
    "@okta/okta-react": { singleton: true },
    // ... other shared deps
  },
  exposes: {
    "./AuthProvider": "./src/providers/AuthProvider",
    "./GlobalConfigProvider": "./src/providers/GlobalConfigProvider",
    "./useAuth": "./src/hooks/useAuth",
  },
});
```

**MFE webpack.config.js** (example: mfe-campaigns):

```javascript
new ModuleFederationPlugin({
  name: "mfe_campaigns",
  filename: "remoteEntry.js",
  exposes: {
    "./App": "./src/App",
    "./Router": "./src/Router",
  },
  remotes: {
    shell: "shell@[shellUrl]/remoteEntry.js",
  },
  shared: {
    react: { singleton: true },
    "react-dom": { singleton: true },
    "react-router-dom": { singleton: true },
    // ... same as shell
  },
});
```

### 4.2 Routing Implementation

**Shell Router**:

```javascript
import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";

const CampaignsMFE = lazy(() => import("mfe_campaigns/App"));
const RewardsMFE = lazy(() => import("mfe_rewards/App"));
// ... other MFEs

function Router() {
  return (
    <Routes>
      <Route path="/" element={<DashboardMFE />} />
      <Route
        path="/campaigns/*"
        element={
          <Suspense fallback={<Loader />}>
            <CampaignsMFE />
          </Suspense>
        }
      />
      <Route
        path="/rewards/*"
        element={
          <Suspense fallback={<Loader />}>
            <RewardsMFE />
          </Suspense>
        }
      />
      {/* ... other routes */}
    </Routes>
  );
}
```

**MFE Internal Router** (mfe-campaigns):

```javascript
function CampaignsRouter() {
  return (
    <Routes>
      <Route path="campaign-list" element={<CampaignListPage />} />
      <Route path="create/*" element={<CampaignSetupOutlet />}>
        <Route path="generic-setup" element={<GenericSetupPage />} />
        <Route path="segment-specific-setup" element={<SegmentSetupPage />} />
        {/* ... wizard steps */}
      </Route>
    </Routes>
  );
}
```

### 4.3 Authentication Flow

```javascript
// Shell: Provides auth context
export function AuthProvider({ children }) {
  const { oktaAuth, authState } = useOktaAuth();

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, oktaAuth }}>
      {children}
    </AuthContext.Provider>
  );
}

// MFE: Consumes auth context
import { useAuth } from "shell/useAuth";

function CampaignList() {
  const { isAuthenticated, user } = useAuth();
  // ... use auth state
}
```

---

## 5. Communication Patterns

### 5.1 Inter-MFE Communication

**Pattern 1: Event Bus** (Preferred for loose coupling)

```javascript
// @loyalty-admin/shared-utils/eventBus.js
import { EventEmitter } from "events";
export const eventBus = new EventEmitter();

// MFE-Campaigns: Emit event
eventBus.emit("campaign:created", { campaignId: "123" });

// MFE-Rewards: Listen to event
eventBus.on("campaign:created", (data) => {
  console.log("Campaign created:", data.campaignId);
});
```

**Pattern 2: Shared State** (Apollo Cache)

```javascript
// Write to cache
client.writeQuery({
  query: GET_SELECTED_CAMPAIGN,
  data: { selectedCampaign: campaign },
});

// Read from cache
const { data } = useQuery(GET_SELECTED_CAMPAIGN);
```

**Pattern 3: URL-Based** (Navigation)

```javascript
// Navigate with context
navigate("/rewards/select?campaignId=123&context=campaign-creation");

// Read context
const searchParams = new URLSearchParams(location.search);
const campaignId = searchParams.get("campaignId");
```

## 6. Local Development

### 6.1 Development Scripts

**package.json (root)**:

```json
{
  "scripts": {
    "dev:shell": "nx serve shell",
    "dev:campaigns": "nx serve mfe-campaigns",
    "dev:rewards": "nx serve mfe-rewards",
    "dev:members": "nx serve mfe-members",
    "dev:content": "nx serve mfe-content",
    "dev:sweepstakes": "nx serve mfe-sweepstakes",
    "dev:support": "nx serve mfe-customer-support",
    "dev:management": "nx serve mfe-management",
    "dev:partners": "nx serve mfe-partners",
    "dev:dashboard": "nx serve mfe-dashboard",

    "dev:all": "concurrently \"npm:dev:*\"",

    "build:shell": "nx build shell --prod",
    "build:all": "nx run-many --target=build --all --parallel=3",

    "test:all": "nx run-many --target=test --all --parallel=3",
    "lint:all": "nx run-many --target=lint --all",

    "storybook": "nx storybook shared-ui"
  }
}
```

### 6.2 Running Local Development

**Terminal 1 - Shell**:

```bash
npm run dev:shell
# Runs on http://localhost:3000
```

**Terminal 2 - Campaigns MFE**:

```bash
npm run dev:campaigns
# Runs on http://localhost:3001
```

**Terminal 3 - Rewards MFE**:

```bash
npm run dev:rewards
# Runs on http://localhost:3002
```

**Or run all together**:

```bash
npm run dev:all
```

### 6.3 Environment Configuration

**.env.development**:

```bash
# Shell
REACT_APP_SHELL_URL=http://localhost:3000

# Microfrontends
REACT_APP_MFE_CAMPAIGNS_URL=http://localhost:3001
REACT_APP_MFE_REWARDS_URL=http://localhost:3002
REACT_APP_MFE_MEMBERS_URL=http://localhost:3003
REACT_APP_MFE_CONTENT_URL=http://localhost:3004
REACT_APP_MFE_SWEEPSTAKES_URL=http://localhost:3005
REACT_APP_MFE_SUPPORT_URL=http://localhost:3006
REACT_APP_MFE_MANAGEMENT_URL=http://localhost:3007
REACT_APP_MFE_PARTNERS_URL=http://localhost:3008
REACT_APP_MFE_DASHBOARD_URL=http://localhost:3009

# Backend
REACT_APP_HOST_API=https://dev-api.loyalty.com/graphql

# Okta
REACT_APP_OKTA_ISSUER=https://dev-okta.loyalty.com/oauth2/default
REACT_APP_OKTA_CLIENT_ID=your-client-id
REACT_APP_OKTA_REDIRECT_URI=/login/callback
```

---
