# Microfrontend Architecture Design
## Loyalty Admin UI - Migration from Monorepo to Microfrontend

> **Document Version**: 1.0.0  
> **Target Architecture**: Module Federation (Webpack 5)  
> **Created**: April 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current State Analysis](#2-current-state-analysis)
3. [Proposed Architecture](#3-proposed-architecture)
4. [Domain Decomposition](#4-domain-decomposition)
5. [Technical Implementation](#5-technical-implementation)
6. [Migration Strategy](#6-migration-strategy)
7. [Communication Patterns](#7-communication-patterns)
8. [State & Routing](#8-state--routing)
9. [Deployment Strategy](#9-deployment-strategy)
10. [Risk Assessment](#10-risk-assessment)

---

## 1. Executive Summary

### Current State
Loyalty Admin UI is a React 18.2 monorepo with **1180+ source files** spanning **20+ feature domains**. Built with Create React App, it manages PepsiCo's loyalty program administration with tight coupling through shared contexts and components.

### Proposed Solution
Migrate to **Module Federation-based microfrontend architecture** with:
- **9 independent microfrontend applications**
- **1 shell application** (host/container)
- **4 shared packages** (ui, utils, types, graphql)

### Key Benefits

| Benefit | Impact |
|---------|--------|
| Independent Deployments | Deploy features without full rebuild (70% faster) |
| Team Autonomy | Teams own domains end-to-end |
| Faster Builds | Build only changed MFEs (~5-10 min vs 30+ min) |
| Technology Flexibility | Upgrade dependencies per MFE |
| Fault Isolation | Failures contained to specific domains |
| Scalability | Scale teams independently |

### Timeline
**Total Duration**: 8-12 months
- Phase 1 (Months 1-3): Foundation & Shell
- Phase 2 (Months 4-9): Domain Migration
- Phase 3 (Months 10-12): Optimization & Cutover

---

## 2. Current State Analysis

### 2.1 Technology Stack

```yaml
Core: React 18.2.0, React Router 6.22.3, CRA 5.0.1
State: Apollo Client 3.9.10, React Context API
UI: Material-UI 5.15.15, PepsiCo DS 2.0.6, Styled Components 6.1.8
Auth: Okta React 6.9.0
Features: GrowthBook 1.3.0
```

### 2.2 Domain Analysis

| Domain | Route | Files | Complexity | Independence |
|--------|-------|-------|------------|--------------|
| Dashboard | `/` | 1 | Low | High |
| **Campaigns** | `/campaigns/*` | 110 | Very High | Medium |
| Rewards | `/rewards/*` | 21 | Medium | High |
| Members | `/member-list/*` | 43 | High | Medium |
| Content | `/content/*` | 18 | Medium | High |
| Sweepstakes | `/sweepstakes/*` | 16 | Medium | High |
| Widgets | `/widgets/*` | 11 | Medium | Medium |
| **Partners** | `/partners/*` | 65 | High | Medium |
| Management | `/system-setting/*` | 31 | Medium | Low |
| Segmentation | `/segmentation/*` | 13 | Medium | Medium |
| Products | `/products/*` | 4 | Low | High |
| Performances | `/performances-list/*` | 11 | Medium | Medium |
| Customer Support | `/customer-support/*` | 2 | Medium | Medium |
| Leaderboards | `/leaderboards/*` | 19 | Medium | Medium |

### 2.3 Shared Resources

**Contexts (25)**: GlobalConfig, Apollo, CampaignSetup, Banner, Survey, Reward, Activity, Partner, etc.

**Common Components (92)**: Header, Sidebar, Tables, Cards, Forms, Modals, Filters, DatePickers, etc.

**Utilities (17)**: commons.js (18k), oktaAuth, featureToggle, bynderSdk, i18n, validateJsonFormsData

**GraphQL**: 41 queries, 30 mutations

### 2.4 Current Pain Points

1. **Monolithic Build**: 5-10 minute full builds
2. **Tight Coupling**: Shared contexts across all domains
3. **Large Bundle**: Initial load ~8-12 MB
4. **Team Blocking**: Cannot deploy independently
5. **Testing Overhead**: Full regression for any change
6. **Tech Debt**: Cannot upgrade incrementally

---

## 3. Proposed Architecture

### 3.1 Architecture Pattern

**Chosen**: Module Federation (Webpack 5)

**Why**:
- ✅ Runtime integration (no build coupling)
- ✅ Shared dependencies (React, MUI, Apollo)
- ✅ Dynamic remote loading
- ✅ Production-ready, React 18+ compatible

### 3.2 High-Level Architecture

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

### 3.3 Package Structure

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

## 4. Domain Decomposition

### 4.1 Shell Application

**Responsibilities**:
- Bootstrap & initialization
- Top-level routing
- Authentication guard (Okta)
- Global layout (Header, Sidebar)
- MFE loading & error boundaries
- Shared providers (Auth, Config, Apollo, Loader, i18n, GrowthBook)

**Exposes**:
```javascript
'./AuthProvider'
'./GlobalConfigProvider'
'./ApolloProvider'
'./LoaderProvider'
'./useAuth'
'./useGlobalConfig'
'./useHasAccessPermission'
'./eventBus'
```

**Bundle Target**: ~500 KB (gzip)

### 4.2 Microfrontend Specifications

#### MFE-Campaigns
- **Routes**: `/campaigns/*` (campaign-list, calendar, create wizard, edit, leaderboards)
- **Features**: 7-step creation wizard, bonus campaigns, leaderboards
- **Components**: 110 files
- **Contexts**: CampaignSetupContext, ActivitySetupContext
- **Dependencies**: Rewards (reward selection), Segmentation, Partners
- **Bundle Target**: ~1.2 MB

#### MFE-Rewards
- **Routes**: `/rewards/*`, `/products/*`, `/winning-rewards-screen/*`
- **Features**: Reward catalogs, reward groups, products
- **Components**: 21 files
- **Context**: RewardContext
- **Dependencies**: Partners (code groups)
- **Bundle Target**: ~400 KB

#### MFE-Members
- **Routes**: `/member-list/*`, `/member/:memberId`
- **Features**: Member search, details, wallet, transactions, participation
- **Components**: 43 files
- **Bundle Target**: ~600 KB

#### MFE-Content
- **Routes**: `/content/*` (pages, banners, surveys, create, edit)
- **Features**: Content creation (image/video/text), banners, surveys
- **Components**: 18 files
- **Contexts**: BannerContext, SurveyContext
- **Dependencies**: Widgets, Bynder SDK
- **Bundle Target**: ~700 KB

#### MFE-Sweepstakes
- **Routes**: `/sweepstakes/*` (winners, active, pick-winners, archiving)
- **Features**: Winner selection, entrant management, archiving
- **Components**: 16 files
- **Bundle Target**: ~350 KB

#### MFE-Customer-Support
- **Routes**: `/customer-support/*` (member-lookup, code-search)
- **Features**: Member lookup, code search
- **Components**: Reuses member components
- **Dependencies**: Members MFE
- **Bundle Target**: ~300 KB

#### MFE-Management
- **Routes**: `/system-setting/*` (T&C, limits, social, widgets, app-config)
- **Features**: System settings, configurations, widgets
- **Components**: 31 files
- **Context**: EditWidgetContext
- **Bundle Target**: ~450 KB

#### MFE-Partners
- **Routes**: `/partners/*`, `/code-groups/*`, `/segmentation/*`
- **Features**: Partners, code groups, segments
- **Components**: 65 partner + 13 segmentation files
- **Context**: PartnerContext
- **Bundle Target**: ~800 KB

#### MFE-Dashboard
- **Routes**: `/` (root), `/performances-list/*`
- **Features**: Dashboard, performance metrics, analytics
- **Components**: 11 files
- **Dependencies**: Recharts
- **Bundle Target**: ~400 KB

### 4.3 Shared Packages

#### Shared-UI (`@loyalty-admin/shared-ui`)
- **Contents**: Layout (Header, Sidebar), Tables, Cards, Forms, Modals, Buttons
- **Distribution**: Module Federation + npm
- **Includes**: Storybook documentation

#### Shared-Utils (`@loyalty-admin/shared-utils`)
- **Contents**: commons.js, functions, constants, featureToggle, configMap

#### Shared-GraphQL (`@loyalty-admin/shared-graphql`)
- **Contents**: Queries, mutations, reusable hooks

#### Shared-Types (`@loyalty-admin/shared-types`)
- **Contents**: TypeScript type definitions

---

## 5. Technical Implementation

### 5.1 Module Federation Config

**Shell webpack.config.js**:
```javascript
new ModuleFederationPlugin({
  name: 'shell',
  remotes: {
    mfe_campaigns: 'mfe_campaigns@[url]/remoteEntry.js',
    mfe_rewards: 'mfe_rewards@[url]/remoteEntry.js',
    // ... other remotes
  },
  shared: {
    react: { singleton: true, eager: true },
    'react-dom': { singleton: true, eager: true },
    'react-router-dom': { singleton: true },
    '@mui/material': { singleton: true },
    '@apollo/client': { singleton: true },
    '@okta/okta-react': { singleton: true },
    // ... other shared deps
  },
  exposes: {
    './AuthProvider': './src/providers/AuthProvider',
    './GlobalConfigProvider': './src/providers/GlobalConfigProvider',
    './useAuth': './src/hooks/useAuth',
  },
});
```

**MFE webpack.config.js** (example: mfe-campaigns):
```javascript
new ModuleFederationPlugin({
  name: 'mfe_campaigns',
  filename: 'remoteEntry.js',
  exposes: {
    './App': './src/App',
    './Router': './src/Router',
  },
  remotes: {
    shell: 'shell@[shellUrl]/remoteEntry.js',
  },
  shared: {
    react: { singleton: true },
    'react-dom': { singleton: true },
    'react-router-dom': { singleton: true },
    // ... same as shell
  },
});
```

### 5.2 Routing Implementation

**Shell Router**:
```javascript
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

const CampaignsMFE = lazy(() => import('mfe_campaigns/App'));
const RewardsMFE = lazy(() => import('mfe_rewards/App'));
// ... other MFEs

function Router() {
  return (
    <Routes>
      <Route path="/" element={<DashboardMFE />} />
      <Route path="/campaigns/*" element={
        <Suspense fallback={<Loader />}>
          <CampaignsMFE />
        </Suspense>
      } />
      <Route path="/rewards/*" element={
        <Suspense fallback={<Loader />}>
          <RewardsMFE />
        </Suspense>
      } />
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

### 5.3 Authentication Flow

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
import { useAuth } from 'shell/useAuth';

function CampaignList() {
  const { isAuthenticated, user } = useAuth();
  // ... use auth state
}
```

---

## 6. Migration Strategy

### 6.1 Migration Roadmap

#### Phase 1: Foundation (Months 1-3)

**Month 1: Monorepo Setup**
- Initialize Nx/Turborepo workspace
- Create package structure
- Configure shared configs (ESLint, TypeScript, Prettier)
- Set up CI/CD templates

**Month 2: Shell & Shared Packages**
- Create shell application
- Migrate authentication (Okta)
- Migrate global providers
- Migrate layout (Header, Sidebar)
- Create shared-ui package (extract 92 common components)
- Create shared-utils, shared-graphql, shared-types
- Set up Storybook

**Month 3: Pilot MFE**
- Create mfe-dashboard (lowest risk)
- Configure Module Federation
- Integrate with shell
- Deploy to dev
- Validate end-to-end flow

**Deliverables**: Shell app, shared packages, 1 pilot MFE deployed

#### Phase 2: Domain Migration (Months 4-9)

**Migration Order** (by complexity & dependencies):

| Month | MFEs | Rationale |
|-------|------|-----------|
| 4 | Rewards, Sweepstakes | Low risk, moderate complexity |
| 5 | Products, Content | Low/medium risk |
| 6 | Members, Customer Support | Medium risk, high complexity |
| 7-8 | Partners, Management | High complexity, many dependencies |
| 9 | Campaigns | Highest complexity (110 files), migrate last |

**Per-MFE Checklist**:
1. Create package structure
2. Configure Module Federation
3. Migrate components & contexts
4. Migrate GraphQL operations
5. Update routing
6. Write integration tests
7. Deploy to dev → QA → prod

**Deliverables**: All 9 MFEs deployed to production

#### Phase 3: Optimization & Cutover (Months 10-12)

**Month 10: Optimization**
- Bundle size optimization
- Code splitting
- Performance tuning
- Security audit

**Month 11: Testing & Validation**
- Load testing
- Full regression testing
- UAT

**Month 12: Cutover**
- Production cutover
- Monitoring
- Bug fixes
- Decommission monolith

**Deliverables**: Optimized architecture, monolith decommissioned

### 6.2 Migration Priority Matrix

| MFE | Priority | Complexity | Risk | Dependencies | Effort |
|-----|----------|------------|------|--------------|--------|
| Dashboard | P1 | Low | Low | Few | 2-3 weeks |
| Rewards | P1 | Medium | Low | Moderate | 4-5 weeks |
| Sweepstakes | P1 | Medium | Low | Few | 3-4 weeks |
| Products | P1 | Low | Low | Few | 1-2 weeks |
| Content | P2 | Medium | Medium | Moderate | 5-6 weeks |
| Members | P2 | High | Medium | Moderate | 6-7 weeks |
| Support | P2 | Medium | Low | High | 3-4 weeks |
| Partners | P2 | High | Medium | High | 7-8 weeks |
| Management | P3 | Medium | High | High | 5-6 weeks |
| **Campaigns** | **P3** | **Very High** | **High** | **Very High** | **10-12 weeks** |

---

## 7. Communication Patterns

### 7.1 Inter-MFE Communication

**Pattern 1: Event Bus** (Preferred for loose coupling)
```javascript
// @loyalty-admin/shared-utils/eventBus.js
import { EventEmitter } from 'events';
export const eventBus = new EventEmitter();

// MFE-Campaigns: Emit event
eventBus.emit('campaign:created', { campaignId: '123' });

// MFE-Rewards: Listen to event
eventBus.on('campaign:created', (data) => {
  console.log('Campaign created:', data.campaignId);
});
```

**Pattern 2: Shared State** (Apollo Cache)
```javascript
// Write to cache
client.writeQuery({
  query: GET_SELECTED_CAMPAIGN,
  data: { selectedCampaign: campaign }
});

// Read from cache
const { data } = useQuery(GET_SELECTED_CAMPAIGN);
```

**Pattern 3: URL-Based** (Navigation)
```javascript
// Navigate with context
navigate('/rewards/select?campaignId=123&context=campaign-creation');

// Read context
const searchParams = new URLSearchParams(location.search);
const campaignId = searchParams.get('campaignId');
```

### 7.2 Cross-Cutting Concerns

**Authentication**:
```javascript
import { useAuth } from 'shell/useAuth';
const { isAuthenticated, user, oktaAuth } = useAuth();
```

**Global Configuration**:
```javascript
import { useGlobalConfig } from 'shell/useGlobalConfig';
const { programConfig, programId, refetchProgramConfig } = useGlobalConfig();
```

**Authorization**:
```javascript
import { useHasAccessPermission } from 'shell/useHasAccessPermission';
const hasPermission = useHasAccessPermission(['campaigns.delete']);
```

---

## 8. State & Routing

### 8.1 State Ownership Levels

```
Level 1: Shell State (Global)
  - Authentication (Okta)
  - Program configuration
  - Multi-program selection
  - Global loading
  - Feature flags

Level 2: MFE State (Domain-Specific)
  - Campaign wizard state (mfe-campaigns)
  - Reward selection state (mfe-rewards)
  - Banner editing state (mfe-content)
  
Level 3: Component State (Local)
  - Form inputs
  - Modal state
  - Pagination
```

### 8.2 Routing Strategy

- **Shell**: Owns top-level routes, loads MFEs
- **MFEs**: Own internal routes (nested)
- **Cross-MFE Navigation**: via `useNavigate()` with URL params

---

## 9. Deployment Strategy

### 9.1 CI/CD Pipeline

**Independent Pipelines**:
```yaml
# Per-MFE pipeline (example: mfe-campaigns)
on:
  push:
    paths:
      - 'packages/mfe-campaigns/**'
      - 'packages/shared-ui/**'

jobs:
  - Lint
  - Test (unit + integration)
  - Build
  - Build Docker image
  - Push to registry
  - Deploy to K8s/CDN
```

**Benefits**:
- Deploy MFE in 5-10 minutes
- No impact on other MFEs
- Shell auto-loads new version (runtime)

### 9.2 Versioning

- **Shell**: Semantic versioning (1.0.0)
- **MFEs**: Independent versions
- **Shared Packages**: Semantic versioning

### 9.3 Deployment Targets

| Environment | Shell URL | MFE URLs |
|-------------|-----------|----------|
| Dev | https://dev-shell.loyalty.com | https://dev-mfe-*.loyalty.com |
| QA | https://qa-shell.loyalty.com | https://qa-mfe-*.loyalty.com |
| Prod | https://admin.loyalty.com | https://mfe-*.loyalty.com |

---

## 10. Risk Assessment

### 10.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Module Federation version conflicts | High | Medium | Lock shared dependency versions |
| Performance degradation | Medium | Low | Load testing, code splitting |
| Cross-MFE communication complexity | Medium | Medium | Event bus pattern, clear contracts |
| Bundle size increase | Low | Low | Proper shared config, monitoring |
| Breaking changes during migration | High | Medium | Feature flags, parallel run |

### 10.2 Organizational Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Team learning curve | Medium | Training, documentation, pilot MFE |
| Coordination overhead | Medium | Clear ownership, autonomous teams |
| Migration timeline slippage | High | Buffer time, prioritize P1 domains |

### 10.3 Rollback Strategy

- Keep monolith deployable during migration
- Feature flags to switch between old/new
- Gradual cutover per domain

---

## Appendices

### A. Key Technologies

- **Webpack 5**: Module Federation
- **Nx/Turborepo**: Monorepo management
- **React 18**: UI framework
- **Apollo Client**: GraphQL & caching
- **Okta**: Authentication
- **Material-UI**: Component library

### B. Reference Documentation

- [Module Federation Docs](https://webpack.js.org/concepts/module-federation/)
- [Nx Workspace](https://nx.dev/)
- [React Router v6](https://reactrouter.com/)
- [Apollo Client](https://www.apollographql.com/docs/react/)

### C. Team Contacts

- Architecture Lead: [Name]
- Frontend Lead: [Name]
- DevOps Lead: [Name]

---

**Document Status**: Draft for Review  
**Next Steps**: Review with stakeholders, refine estimates, begin Phase 1
