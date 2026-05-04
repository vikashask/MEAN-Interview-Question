# Microfrontend Implementation Guide
## Loyalty Admin UI - Step-by-Step Technical Implementation

> **Companion Document**: MICROFRONTEND_ARCHITECTURE.md  
> **Version**: 1.0.0  
> **Audience**: Development Teams

---

## Table of Contents

1. [Development Environment Setup](#1-development-environment-setup)
2. [Shell Application Implementation](#2-shell-application-implementation)
3. [Microfrontend Implementation](#3-microfrontend-implementation)
4. [Shared Packages Setup](#4-shared-packages-setup)
5. [Local Development](#5-local-development)
6. [Testing Strategies](#6-testing-strategies)
7. [Deployment Configuration](#7-deployment-configuration)
8. [Migration Checklist](#8-migration-checklist)

---

## 1. Development Environment Setup

### 1.1 Prerequisites

```bash
Node.js: v18.x or higher
npm: v9.x or higher
Docker: 20.x or higher (for containerization)
Git: 2.x or higher
```

### 1.2 Initialize Nx Workspace

```bash
# Install Nx globally
npm install -g nx

# Create Nx workspace
npx create-nx-workspace@latest loyalty-admin-ui \
  --preset=empty \
  --packageManager=npm

cd loyalty-admin-ui

# Install required plugins
npm install -D @nrwl/react @nrwl/webpack @nrwl/jest @nrwl/storybook
npm install -D @module-federation/enhanced
```

### 1.3 Workspace Configuration

**nx.json**:
```json
{
  "npmScope": "loyalty-admin",
  "affected": {
    "defaultBase": "main"
  },
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx/tasks-runners/default",
      "options": {
        "cacheableOperations": ["build", "test", "lint"]
      }
    }
  },
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"]
    }
  },
  "workspaceLayout": {
    "appsDir": "packages",
    "libsDir": "packages"
  }
}
```

### 1.4 TypeScript Configuration

**tsconfig.base.json**:
```json
{
  "compileOnSave": false,
  "compilerOptions": {
    "rootDir": ".",
    "sourceMap": true,
    "declaration": false,
    "moduleResolution": "node",
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "importHelpers": true,
    "target": "es2015",
    "module": "esnext",
    "lib": ["es2020", "dom"],
    "skipLibCheck": true,
    "skipDefaultLibCheck": true,
    "baseUrl": ".",
    "paths": {
      "@loyalty-admin/shared-ui": ["packages/shared-ui/src/index.ts"],
      "@loyalty-admin/shared-utils": ["packages/shared-utils/src/index.ts"],
      "@loyalty-admin/shared-types": ["packages/shared-types/src/index.ts"],
      "@loyalty-admin/shared-graphql": ["packages/shared-graphql/src/index.ts"]
    },
    "jsx": "react-jsx"
  },
  "exclude": ["node_modules", "tmp"]
}
```

---

## 2. Shell Application Implementation

### 2.1 Create Shell Package

```bash
# Generate shell application
nx g @nrwl/react:app shell --style=scss --routing=true --bundler=webpack
```

### 2.2 Shell Webpack Configuration

**packages/shell/webpack.config.js**:
```javascript
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { dependencies } = require('./package.json');

// Environment-specific URLs for remotes
const getRemoteUrl = (name, port) => {
  const env = process.env.NODE_ENV || 'development';
  const urls = {
    development: `http://localhost:${port}`,
    qa: `https://qa-${name}.loyalty-admin.com`,
    production: `https://${name}.loyalty-admin.com`
  };
  return urls[env];
};

module.exports = {
  entry: './src/index',
  mode: process.env.NODE_ENV || 'development',
  
  devServer: {
    port: 3000,
    historyApiFallback: true,
    hot: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  },
  
  output: {
    publicPath: 'auto',
    clean: true,
  },
  
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
  },
  
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-react',
              '@babel/preset-typescript',
            ],
            plugins: [
              '@babel/plugin-transform-runtime',
            ],
          },
        },
      },
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        type: 'asset/resource',
      },
    ],
  },
  
  plugins: [
    new ModuleFederationPlugin({
      name: 'shell',
      filename: 'remoteEntry.js',
      
      remotes: {
        mfe_campaigns: `mfe_campaigns@${getRemoteUrl('mfe-campaigns', 3001)}/remoteEntry.js`,
        mfe_rewards: `mfe_rewards@${getRemoteUrl('mfe-rewards', 3002)}/remoteEntry.js`,
        mfe_members: `mfe_members@${getRemoteUrl('mfe-members', 3003)}/remoteEntry.js`,
        mfe_content: `mfe_content@${getRemoteUrl('mfe-content', 3004)}/remoteEntry.js`,
        mfe_sweepstakes: `mfe_sweepstakes@${getRemoteUrl('mfe-sweepstakes', 3005)}/remoteEntry.js`,
        mfe_customer_support: `mfe_customer_support@${getRemoteUrl('mfe-customer-support', 3006)}/remoteEntry.js`,
        mfe_management: `mfe_management@${getRemoteUrl('mfe-management', 3007)}/remoteEntry.js`,
        mfe_partners: `mfe_partners@${getRemoteUrl('mfe-partners', 3008)}/remoteEntry.js`,
        mfe_dashboard: `mfe_dashboard@${getRemoteUrl('mfe-dashboard', 3009)}/remoteEntry.js`,
      },
      
      shared: {
        react: {
          singleton: true,
          requiredVersion: dependencies.react,
          eager: true,
        },
        'react-dom': {
          singleton: true,
          requiredVersion: dependencies['react-dom'],
          eager: true,
        },
        'react-router-dom': {
          singleton: true,
          requiredVersion: dependencies['react-router-dom'],
        },
        '@mui/material': {
          singleton: true,
          requiredVersion: dependencies['@mui/material'],
        },
        '@mui/icons-material': {
          singleton: true,
        },
        '@emotion/react': {
          singleton: true,
        },
        '@emotion/styled': {
          singleton: true,
        },
        '@apollo/client': {
          singleton: true,
          requiredVersion: dependencies['@apollo/client'],
        },
        '@okta/okta-react': {
          singleton: true,
        },
        '@okta/okta-auth-js': {
          singleton: true,
        },
        'styled-components': {
          singleton: true,
        },
        'moment-timezone': {
          singleton: true,
        },
        'graphql': {
          singleton: true,
        },
        'i18next': {
          singleton: true,
        },
        'react-i18next': {
          singleton: true,
        },
        'lodash': {},
      },
      
      exposes: {
        './AuthProvider': './src/providers/AuthProvider',
        './GlobalConfigProvider': './src/providers/GlobalConfigProvider',
        './ApolloProvider': './src/providers/ApolloProvider',
        './LoaderProvider': './src/providers/LoaderProvider',
        './useAuth': './src/hooks/useAuth',
        './useGlobalConfig': './src/hooks/useGlobalConfig',
        './useLoader': './src/hooks/useLoader',
        './useHasAccessPermission': './src/hooks/useHasAccessPermission',
        './eventBus': './src/utils/eventBus',
        './Navigation': './src/components/Navigation',
      },
    }),
    
    new HtmlWebpackPlugin({
      template: './public/index.html',
      inject: 'body',
    }),
  ],
};
```

### 2.3 Shell Application Structure

```
packages/shell/
├── src/
│   ├── index.tsx                 # Entry point
│   ├── App.tsx                   # Main app component
│   ├── bootstrap.tsx             # Dynamic import for Module Federation
│   ├── providers/
│   │   ├── AuthProvider.tsx
│   │   ├── GlobalConfigProvider.tsx
│   │   ├── ApolloProvider.tsx
│   │   └── LoaderProvider.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useGlobalConfig.ts
│   │   ├── useLoader.ts
│   │   └── useHasAccessPermission.ts
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── MainLayout.tsx
│   │   ├── Navigation/
│   │   │   └── Navigation.tsx
│   │   ├── ErrorBoundary/
│   │   │   └── MFEErrorBoundary.tsx
│   │   └── LoadingFallback/
│   │       └── LoadingFallback.tsx
│   ├── routes/
│   │   └── Router.tsx
│   ├── utils/
│   │   ├── oktaAuth.ts
│   │   ├── eventBus.ts
│   │   └── mfeLoader.ts
│   └── types/
│       └── index.ts
├── public/
│   ├── index.html
│   └── config.js              # Runtime config
├── webpack.config.js
├── package.json
└── tsconfig.json
```

### 2.4 Shell App.tsx Implementation

**packages/shell/src/App.tsx**:
```typescript
import React from 'react';
import { Security } from '@okta/okta-react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { I18nextProvider } from 'react-i18next';
import { GrowthBookProvider } from '@growthbook/growthbook-react';

import { AuthProvider } from './providers/AuthProvider';
import { GlobalConfigProvider } from './providers/GlobalConfigProvider';
import { ApolloProvider } from './providers/ApolloProvider';
import { LoaderProvider } from './providers/LoaderProvider';
import Router from './routes/Router';
import { oktaAuth } from './utils/oktaAuth';
import { growthbook } from './utils/growthbook';
import { theme } from './theme';
import i18n from './utils/i18n';

function App() {
  const customAuthHandler = async () => {
    const previousAuthState = oktaAuth.authStateManager.getPreviousAuthState();
    if (!previousAuthState || !previousAuthState.isAuthenticated) {
      await oktaAuth.signInWithRedirect();
    }
  };

  const restoreOriginalUri = async (_oktaAuth: any, originalUri: string) => {
    window.location.replace(originalUri || '/');
  };

  return (
    <React.StrictMode>
      <I18nextProvider i18n={i18n}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Security
            oktaAuth={oktaAuth}
            onAuthRequired={customAuthHandler}
            restoreOriginalUri={restoreOriginalUri}
          >
            <AuthProvider>
              <LoaderProvider>
                <GlobalConfigProvider>
                  <ApolloProvider>
                    <GrowthBookProvider growthbook={growthbook}>
                      <BrowserRouter>
                        <Router />
                      </BrowserRouter>
                    </GrowthBookProvider>
                  </ApolloProvider>
                </GlobalConfigProvider>
              </LoaderProvider>
            </AuthProvider>
          </Security>
        </ThemeProvider>
      </I18nextProvider>
    </React.StrictMode>
  );
}

export default App;
```

### 2.5 Shell Router with MFE Loading

**packages/shell/src/routes/Router.tsx**:
```typescript
import React, { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useOktaAuth } from '@okta/okta-react';
import MainLayout from '../components/Layout/MainLayout';
import MFEErrorBoundary from '../components/ErrorBoundary/MFEErrorBoundary';
import LoadingFallback from '../components/LoadingFallback/LoadingFallback';
import NotFoundPage from '../pages/NotFoundPage';

// Lazy load microfrontends
const DashboardMFE = lazy(() => import('mfe_dashboard/App'));
const CampaignsMFE = lazy(() => import('mfe_campaigns/App'));
const RewardsMFE = lazy(() => import('mfe_rewards/App'));
const MembersMFE = lazy(() => import('mfe_members/App'));
const ContentMFE = lazy(() => import('mfe_content/App'));
const SweepstakesMFE = lazy(() => import('mfe_sweepstakes/App'));
const CustomerSupportMFE = lazy(() => import('mfe_customer_support/App'));
const ManagementMFE = lazy(() => import('mfe_management/App'));
const PartnersMFE = lazy(() => import('mfe_partners/App'));

function Router() {
  const { authState } = useOktaAuth();

  if (!authState || !authState.isAuthenticated) {
    return <LoadingFallback />;
  }

  return (
    <MainLayout>
      <Routes>
        <Route
          path="/"
          element={
            <MFEErrorBoundary mfeName="Dashboard">
              <Suspense fallback={<LoadingFallback />}>
                <DashboardMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/campaigns/*"
          element={
            <MFEErrorBoundary mfeName="Campaigns">
              <Suspense fallback={<LoadingFallback />}>
                <CampaignsMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/rewards/*"
          element={
            <MFEErrorBoundary mfeName="Rewards">
              <Suspense fallback={<LoadingFallback />}>
                <RewardsMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/member-list/*"
          element={
            <MFEErrorBoundary mfeName="Members">
              <Suspense fallback={<LoadingFallback />}>
                <MembersMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/content/*"
          element={
            <MFEErrorBoundary mfeName="Content">
              <Suspense fallback={<LoadingFallback />}>
                <ContentMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/sweepstakes/*"
          element={
            <MFEErrorBoundary mfeName="Sweepstakes">
              <Suspense fallback={<LoadingFallback />}>
                <SweepstakesMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/customer-support/*"
          element={
            <MFEErrorBoundary mfeName="Customer Support">
              <Suspense fallback={<LoadingFallback />}>
                <CustomerSupportMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/system-setting/*"
          element={
            <MFEErrorBoundary mfeName="Management">
              <Suspense fallback={<LoadingFallback />}>
                <ManagementMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/partners/*"
          element={
            <MFEErrorBoundary mfeName="Partners">
              <Suspense fallback={<LoadingFallback />}>
                <PartnersMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/segmentation/*"
          element={
            <MFEErrorBoundary mfeName="Partners">
              <Suspense fallback={<LoadingFallback />}>
                <PartnersMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/code-groups/*"
          element={
            <MFEErrorBoundary mfeName="Partners">
              <Suspense fallback={<LoadingFallback />}>
                <PartnersMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route
          path="/performances-list/*"
          element={
            <MFEErrorBoundary mfeName="Dashboard">
              <Suspense fallback={<LoadingFallback />}>
                <DashboardMFE />
              </Suspense>
            </MFEErrorBoundary>
          }
        />

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </MainLayout>
  );
}

export default Router;
```

### 2.6 MFE Error Boundary

**packages/shell/src/components/ErrorBoundary/MFEErrorBoundary.tsx**:
```typescript
import React, { Component, ReactNode } from 'react';
import { Alert, Button, Box, Typography } from '@mui/material';

interface Props {
  children: ReactNode;
  mfeName: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class MFEErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error(`Error in ${this.props.mfeName} MFE:`, error, errorInfo);
    
    // Send to monitoring service
    if (window.analytics) {
      window.analytics.track('MFE Error', {
        mfeName: this.props.mfeName,
        error: error.message,
        stack: error.stack,
      });
    }
  }

  handleReload = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <Box sx={{ p: 3 }}>
          <Alert severity="error">
            <Typography variant="h6">
              {this.props.mfeName} Failed to Load
            </Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              {this.state.error?.message || 'An unexpected error occurred'}
            </Typography>
            <Button
              variant="contained"
              onClick={this.handleReload}
              sx={{ mt: 2 }}
            >
              Reload Application
            </Button>
          </Alert>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default MFEErrorBoundary;
```

### 2.7 Event Bus Implementation

**packages/shell/src/utils/eventBus.ts**:
```typescript
import { EventEmitter } from 'events';

class MFEEventBus extends EventEmitter {
  private static instance: MFEEventBus;

  private constructor() {
    super();
    this.setMaxListeners(50); // Increase for multiple MFEs
  }

  static getInstance(): MFEEventBus {
    if (!MFEEventBus.instance) {
      MFEEventBus.instance = new MFEEventBus();
    }
    return MFEEventBus.instance;
  }

  // Type-safe event emitter
  emitEvent<T = any>(event: string, data: T): void {
    this.emit(event, data);
    console.log(`[EventBus] Emitted: ${event}`, data);
  }

  // Type-safe event listener
  onEvent<T = any>(event: string, callback: (data: T) => void): void {
    this.on(event, callback);
    console.log(`[EventBus] Subscribed: ${event}`);
  }

  // Cleanup
  offEvent<T = any>(event: string, callback: (data: T) => void): void {
    this.off(event, callback);
    console.log(`[EventBus] Unsubscribed: ${event}`);
  }
}

export const eventBus = MFEEventBus.getInstance();

// Event type definitions
export interface MFEEvents {
  'campaign:created': { campaignId: string };
  'campaign:updated': { campaignId: string };
  'campaign:deleted': { campaignId: string };
  'reward:selected': { rewardId: string; context?: string };
  'member:updated': { memberId: string };
  'navigation:changed': { path: string };
}
```

---

## 3. Microfrontend Implementation

### 3.1 Create Microfrontend Package (Example: mfe-campaigns)

```bash
# Generate campaigns microfrontend
nx g @nrwl/react:app mfe-campaigns --style=scss --routing=true --bundler=webpack
```

### 3.2 MFE Webpack Configuration

**packages/mfe-campaigns/webpack.config.js**:
```javascript
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');
const { dependencies } = require('./package.json');

module.exports = {
  entry: './src/index',
  mode: process.env.NODE_ENV || 'development',
  
  devServer: {
    port: 3001,
    historyApiFallback: true,
    hot: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  },
  
  output: {
    publicPath: 'auto',
    uniqueName: 'mfe_campaigns',
  },
  
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
  },
  
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
    ],
  },
  
  plugins: [
    new ModuleFederationPlugin({
      name: 'mfe_campaigns',
      filename: 'remoteEntry.js',
      
      exposes: {
        './App': './src/App',
      },
      
      remotes: {
        shell: 'shell@http://localhost:3000/remoteEntry.js',
      },
      
      shared: {
        react: {
          singleton: true,
          requiredVersion: dependencies.react,
        },
        'react-dom': {
          singleton: true,
          requiredVersion: dependencies['react-dom'],
        },
        'react-router-dom': { singleton: true },
        '@mui/material': { singleton: true },
        '@apollo/client': { singleton: true },
        '@okta/okta-react': { singleton: true },
        'styled-components': { singleton: true },
        'moment-timezone': { singleton: true },
        'graphql': { singleton: true },
        'lodash': {},
      },
    }),
  ],
};
```

### 3.3 MFE App Component

**packages/mfe-campaigns/src/App.tsx**:
```typescript
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { CampaignSetupProvider } from './context/CampaignSetupContext';

// Import hooks from shell
import { useAuth } from 'shell/useAuth';
import { useGlobalConfig } from 'shell/useGlobalConfig';

// Pages
import CampaignListPage from './pages/CampaignListPage';
import CampaignCalendarPage from './pages/CampaignCalendarPage';
import BonusListPage from './pages/BonusListPage';
import CampaignSummaryViewPage from './pages/CampaignSummaryViewPage';
import CampaignSetupOutlet from './pages/setup/CampaignSetupOutlet';
import GenericSetupPage from './pages/setup/GenericSetupPage';
import SegmentSetupPage from './pages/setup/SegmentSetupPage';
import ActivitiesSetupPage from './pages/setup/ActivitiesSetupPage';
import CampaignLevelSetupPage from './pages/setup/CampaignLevelSetupPage';
import RulesAndOutcomesPage from './pages/setup/RulesAndOutcomesPage';
import SummaryPage from './pages/setup/SummaryPage';

function App() {
  const { isAuthenticated } = useAuth();
  const { programConfig } = useGlobalConfig();

  if (!isAuthenticated) {
    return null; // Shell handles redirect
  }

  return (
    <CampaignSetupProvider>
      <Routes>
        <Route index element={<Navigate to="campaign-list" replace />} />
        <Route path="campaign-list" element={<CampaignListPage />} />
        <Route path="campaign-calendar" element={<CampaignCalendarPage />} />
        <Route path="bonus-list" element={<BonusListPage />} />
        <Route path="campaign-summary-view/:id" element={<CampaignSummaryViewPage />} />
        
        <Route path="create" element={<CampaignSetupOutlet />}>
          <Route path="generic-setup" element={<GenericSetupPage />} />
          <Route path="segment-specific-setup" element={<SegmentSetupPage />} />
          <Route path="activity-level-setup-new/*" element={<ActivitiesSetupPage />} />
          <Route path="campaign-level-setup" element={<CampaignLevelSetupPage />} />
          <Route path="rules-and-outcomes" element={<RulesAndOutcomesPage />} />
          <Route path="summary" element={<SummaryPage />} />
          <Route index element={<Navigate to="generic-setup" replace />} />
        </Route>
        
        <Route path="edit/:campaignId" element={<CampaignSetupOutlet />}>
          <Route path="generic-setup" element={<GenericSetupPage />} />
          <Route path="segment-specific-setup" element={<SegmentSetupPage />} />
          <Route path="activity-level-setup-new/*" element={<ActivitiesSetupPage />} />
          <Route path="campaign-level-setup" element={<CampaignLevelSetupPage />} />
          <Route path="rules-and-outcomes" element={<RulesAndOutcomesPage />} />
          <Route path="summary" element={<SummaryPage />} />
        </Route>
        
        <Route path="*" element={<Navigate to="campaign-list" replace />} />
      </Routes>
    </CampaignSetupProvider>
  );
}

export default App;
```

### 3.4 Cross-MFE Communication Example

**Navigate to Rewards MFE from Campaigns**:
```typescript
// In mfe-campaigns/src/pages/setup/CampaignLevelSetupPage.tsx
import { useNavigate } from 'react-router-dom';
import { eventBus } from 'shell/eventBus';

function CampaignLevelSetupPage() {
  const navigate = useNavigate();
  const campaignId = '123'; // From context or state

  const handleSelectReward = () => {
    // Navigate to rewards MFE with context
    navigate(`/rewards?context=campaign-creation&campaignId=${campaignId}`);
    
    // Optionally emit event
    eventBus.emitEvent('campaign:reward-selection-started', {
      campaignId,
      timestamp: Date.now(),
    });
  };

  return (
    <div>
      <button onClick={handleSelectReward}>Select Reward</button>
    </div>
  );
}
```

**Listen for reward selection in Rewards MFE**:
```typescript
// In mfe-rewards/src/pages/RewardsPage.tsx
import { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { eventBus } from 'shell/eventBus';

function RewardsPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  const context = searchParams.get('context');
  const campaignId = searchParams.get('campaignId');

  useEffect(() => {
    // Listen for reward selection completion
    const handleRewardSelected = (data: { rewardId: string }) => {
      if (context === 'campaign-creation') {
        // Navigate back to campaigns with selected reward
        navigate(`/campaigns/create/campaign-level-setup?rewardId=${data.rewardId}&campaignId=${campaignId}`);
      }
    };

    eventBus.onEvent('reward:selected', handleRewardSelected);

    return () => {
      eventBus.offEvent('reward:selected', handleRewardSelected);
    };
  }, [context, campaignId, navigate]);

  const handleRewardSelect = (rewardId: string) => {
    // Emit event when reward is selected
    eventBus.emitEvent('reward:selected', { rewardId });
  };

  return <div>Rewards List...</div>;
}
```

---

## 4. Shared Packages Setup

### 4.1 Shared-UI Package

```bash
# Generate shared-ui library
nx g @nrwl/react:library shared-ui --publishable --importPath=@loyalty-admin/shared-ui
```

**packages/shared-ui/package.json**:
```json
{
  "name": "@loyalty-admin/shared-ui",
  "version": "1.0.0",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "peerDependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@mui/material": "^5.15.15"
  }
}
```

**packages/shared-ui/src/index.ts**:
```typescript
// Layout Components
export { default as Header } from './components/Layout/Header';
export { default as Sidebar } from './components/Layout/Sidebar';
export { default as MainCard } from './components/Layout/MainCard';

// Tables
export { default as CommonTable } from './components/Tables/CommonTable';
export { default as StackTable } from './components/Tables/StackTable';

// Cards
export { default as GridCard } from './components/Cards/GridCard';
export { default as StatusTag } from './components/Cards/StatusTag';

// Forms
export { default as DatePickerMaterialUI } from './components/Forms/DatePickerMaterialUI';
export { default as CustomTimePicker } from './components/Forms/CustomTimePicker';
export { default as FilterPopover } from './components/Forms/FilterPopover';

// Modals
export { default as ModalConfirm } from './components/Modals/ModalConfirm';
export { default as ToastNotification } from './components/Modals/ToastNotification';

// Utilities
export * from './utils';
export * from './types';
```

### 4.2 Shared-Utils Package

```bash
nx g @nrwl/js:library shared-utils --publishable --importPath=@loyalty-admin/shared-utils
```

**packages/shared-utils/src/index.ts**:
```typescript
export * from './commons';
export * from './functions';
export * from './constants';
export * from './featureToggle';
export * from './configMap';
export * from './validateJsonFormsData';
```

### 4.3 Storybook Setup for Shared-UI

```bash
# Generate Storybook configuration
nx g @nrwl/react:storybook-configuration shared-ui
```

**Run Storybook**:
```bash
nx storybook shared-ui
```

---

## 5. Local Development

### 5.1 Development Scripts

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

### 5.2 Running Local Development

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

### 5.3 Environment Configuration

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

## 6. Testing Strategies

### 6.1 Unit Testing (Jest)

**packages/mfe-campaigns/src/pages/CampaignListPage.test.tsx**:
```typescript
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import CampaignListPage from './CampaignListPage';

// Mock shell dependencies
jest.mock('shell/useAuth', () => ({
  useAuth: () => ({ isAuthenticated: true, user: { email: 'test@test.com' } })
}));

jest.mock('shell/useGlobalConfig', () => ({
  useGlobalConfig: () => ({ programConfig: { id: '123' } })
}));

describe('CampaignListPage', () => {
  it('renders campaign list', () => {
    render(
      <BrowserRouter>
        <CampaignListPage />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/campaigns/i)).toBeInTheDocument();
  });
});
```

### 6.2 Integration Testing

**packages/shell/src/routes/Router.integration.test.tsx**:
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import App from '../App';

describe('MFE Integration', () => {
  it('loads campaigns MFE when navigating to /campaigns', async () => {
    render(<App />);
    
    act(() => {
      window.history.pushState({}, '', '/campaigns');
    });
    
    await waitFor(() => {
      expect(screen.getByText(/campaign list/i)).toBeInTheDocument();
    });
  });
});
```

### 6.3 E2E Testing (Playwright)

**e2e/campaigns.spec.ts**:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Campaigns MFE', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
    // Login
    await page.fill('[name="username"]', 'testuser');
    await page.fill('[name="password"]', 'password');
    await page.click('[type="submit"]');
  });

  test('should navigate to campaigns and load MFE', async ({ page }) => {
    await page.click('text=Campaigns');
    await expect(page).toHaveURL(/.*campaigns/);
    await expect(page.locator('text=Campaign List')).toBeVisible();
  });

  test('should create a new campaign', async ({ page }) => {
    await page.goto('http://localhost:3000/campaigns/create/generic-setup');
    await page.fill('[name="campaignName"]', 'Test Campaign');
    await page.click('text=Next');
    // ... continue wizard
  });
});
```

---

## 7. Deployment Configuration

### 7.1 Dockerfile for MFE

**packages/mfe-campaigns/Dockerfile**:
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy root package files
COPY package.json package-lock.json ./
COPY nx.json tsconfig.base.json ./

# Copy shared packages
COPY packages/shared-ui ./packages/shared-ui
COPY packages/shared-utils ./packages/shared-utils
COPY packages/shared-types ./packages/shared-types
COPY packages/shared-graphql ./packages/shared-graphql

# Copy MFE
COPY packages/mfe-campaigns ./packages/mfe-campaigns

# Install dependencies
RUN npm ci

# Build MFE
RUN npx nx build mfe-campaigns --prod

# Production image
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/dist/packages/mfe-campaigns /usr/share/nginx/html

# Copy nginx config
COPY packages/mfe-campaigns/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf**:
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Enable gzip
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Handle client-side routing
    location / {
        try_files $uri $uri/ /index.html;
        add_header Access-Control-Allow-Origin *;
    }

    # Health check
    location /health {
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### 7.2 Kubernetes Deployment

**packages/mfe-campaigns/k8s/deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mfe-campaigns
  namespace: loyalty-admin
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mfe-campaigns
  template:
    metadata:
      labels:
        app: mfe-campaigns
    spec:
      containers:
      - name: mfe-campaigns
        image: loyalty-admin/mfe-campaigns:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: mfe-campaigns
  namespace: loyalty-admin
spec:
  selector:
    app: mfe-campaigns
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mfe-campaigns
  namespace: loyalty-admin
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - mfe-campaigns.loyalty-admin.com
    secretName: mfe-campaigns-tls
  rules:
  - host: mfe-campaigns.loyalty-admin.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mfe-campaigns
            port:
              number: 80
```

---

## 8. Migration Checklist

### 8.1 Pre-Migration Checklist

- [ ] Review current architecture documentation
- [ ] Identify all domain boundaries
- [ ] Map dependencies between domains
- [ ] Inventory shared components and utilities
- [ ] Set up Nx/Turborepo workspace
- [ ] Configure Module Federation
- [ ] Set up CI/CD templates
- [ ] Prepare monitoring and observability tools

### 8.2 Shell Migration Checklist

- [ ] Create shell package
- [ ] Migrate authentication (Okta)
- [ ] Migrate global providers (GlobalConfig, Apollo, Loader)
- [ ] Migrate layout components (Header, Sidebar)
- [ ] Set up Module Federation configuration
- [ ] Implement MFE loading infrastructure
- [ ] Create error boundaries
- [ ] Create loading fallbacks
- [ ] Set up event bus
- [ ] Write shell integration tests
- [ ] Deploy shell to dev environment

### 8.3 Per-MFE Migration Checklist

For each microfrontend:

- [ ] Create MFE package structure
- [ ] Configure webpack with Module Federation
- [ ] Migrate domain-specific components
- [ ] Migrate domain-specific contexts
- [ ] Migrate GraphQL operations
- [ ] Update routing (nested routes)
- [ ] Consume shell providers (useAuth, useGlobalConfig)
- [ ] Implement cross-MFE communication (event bus, URL params)
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Update documentation
- [ ] Deploy to dev environment
- [ ] Run smoke tests
- [ ] Deploy to QA environment
- [ ] Run full regression tests
- [ ] Deploy to production
- [ ] Monitor for issues

### 8.4 Shared Packages Checklist

- [ ] Create shared-ui package
- [ ] Extract common components (92 files)
- [ ] Set up Storybook
- [ ] Write component documentation
- [ ] Create shared-utils package
- [ ] Extract utility functions
- [ ] Create shared-graphql package
- [ ] Extract queries and mutations
- [ ] Create shared-types package
- [ ] Publish packages to registry (or configure Module Federation)

### 8.5 Post-Migration Checklist

- [ ] Verify all MFEs deployed to production
- [ ] Run full end-to-end tests
- [ ] Load testing
- [ ] Performance benchmarking
- [ ] Security audit
- [ ] Update team documentation
- [ ] Conduct team training
- [ ] Monitor production metrics
- [ ] Decommission monolith
- [ ] Archive old codebase

---

## Conclusion

This implementation guide provides step-by-step instructions for migrating the Loyalty Admin UI from a monorepo to a microfrontend architecture. Follow the checklist carefully, and migrate one domain at a time to minimize risk.

**Key Success Factors**:
- Start with low-risk domains (Dashboard, Rewards)
- Test thoroughly at each stage
- Use feature flags for gradual rollout
- Monitor performance and errors
- Keep teams aligned through documentation

For questions or issues, refer to the main architecture document (MICROFRONTEND_ARCHITECTURE.md) or contact the architecture team.
