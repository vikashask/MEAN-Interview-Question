# Micro Frontends — Senior Front-End Architect Interview Revision Guide

## 1. Core Concepts — MUST KNOW

- [ ] What is Micro Frontend?
- [ ] Why Micro Frontends?
- [ ] What problem does it solve?
- [ ] Difference between Monolith vs Micro Frontend vs Microservices
- [ ] Relationship between Micro Frontend and Microservices
- [ ] Business-domain-oriented frontend architecture
- [ ] Independent team ownership
- [ ] Independent development
- [ ] Independent deployment
- [ ] Independent versioning
- [ ] Independent scaling
- [ ] Independent technology choice
- [ ] Independent release lifecycle
- [ ] What does "independent" actually mean?
- [ ] When Micro Frontends are useful
- [ ] When Micro Frontends are unnecessary
- [ ] Micro Frontend anti-patterns



### Key interview statement

> Micro Frontends apply the principles of microservices to the frontend, but the primary goal is not simply splitting the UI. The goal is independent domain ownership, development, testing, deployment, and evolution while providing a seamless user experience.

---



## 2. Architecture Patterns

Know these patterns very well:

- [ ] Build-time integration
- [ ] Server-side integration
- [ ] Edge-side integration
- [ ] Client-side/runtime integration
- [ ] iframe-based integration
- [ ] Web Components
- [ ] JavaScript integration
- [ ] Module Federation
- [ ] Single-SPA
- [ ] Route-based composition
- [ ] Application-shell architecture



### Architecture

```text
                    Micro Frontends
                          |
       +------------------+------------------+
       |                  |                  |
   Build Time        Server Side        Runtime
       |                  |                  |
    npm package       SSR/ESI          Module Federation
       |                  |                  |
       +------------------+------------------+
                          |
                    Application Shell
                          |
        +-----------------+----------------+
        |                 |                |
      Orders            Users           Payments
        |                 |                |
       Team A            Team B           Team C
```

---



## 3. Application Shell / Container

Know:

- [ ] What is Application Shell?
- [ ] What responsibilities belong to Shell?
- [ ] Routing
- [ ] Authentication
- [ ] Authorization
- [ ] Global navigation
- [ ] Layout
- [ ] Error boundaries
- [ ] Loading states
- [ ] Feature flags
- [ ] Global configuration
- [ ] Telemetry
- [ ] Session management
- [ ] Cross-MFE communication
- [ ] Remote loading
- [ ] Version compatibility

```text
                 Browser
                    |
             Application Shell
                    |
        +-----------+-----------+
        |           |           |
      MFE A       MFE B       MFE C
      Orders       Users      Payments
        |           |           |
      Team A      Team B      Team C
```



### Interview question

**What should NOT be placed inside the shell?**

Avoid turning the shell into a new monolith. The shell should not contain domain-specific business logic belonging to individual MFEs.

---



## 4. Domain Decomposition

This is one of the most important architect-level topics.

### Bad decomposition

```text
Header MFE
Button MFE
Table MFE
Modal MFE
Footer MFE
```



### Better decomposition

```text
Customer MFE
Order MFE
Payment MFE
Inventory MFE
Reporting MFE
```

Know:

- [ ] Domain-driven decomposition
- [ ] Business capability boundaries
- [ ] Bounded contexts
- [ ] Team ownership
- [ ] Conway's Law
- [ ] Organizational boundaries
- [ ] Domain coupling
- [ ] Shared domain ownership problems



### Interview question

**How would you identify MFE boundaries?**

Start from business capabilities and team ownership rather than UI components. Consider domain boundaries, release independence, data ownership, organizational structure, and coupling.

---



## 5. Module Federation — VERY IMPORTANT

For modern React architect roles, this is one of the highest-priority topics.

Know:

- [ ] What is Module Federation?
- [ ] Webpack Module Federation
- [ ] Runtime module loading
- [ ] Host
- [ ] Remote
- [ ] Remote Entry
- [ ] Exposes
- [ ] Remotes
- [ ] Shared dependencies
- [ ] Singleton
- [ ] Eager loading
- [ ] Lazy loading
- [ ] Version negotiation
- [ ] Dependency sharing
- [ ] Runtime loading
- [ ] Remote versioning
- [ ] Remote deployment
- [ ] Remote failure
- [ ] Fallback strategies

```text
Host / Shell
     |
     +------ Remote A
     |       Orders
     |
     +------ Remote B
     |       Customers
     |
     +------ Remote C
             Payments
```

---



## 6. Module Federation Configuration

Be comfortable explaining concepts like:

```javascript
new ModuleFederationPlugin({
  name: "host",

  remotes: {
    orders: "orders@https://orders.example.com/remoteEntry.js"
  },

  shared: {
    react: {
      singleton: true
    },
    "react-dom": {
      singleton: true
    }
  }
})
```

Know what each means:

- [ ] `name`
- [ ] `remotes`
- [ ] `exposes`
- [ ] `shared`
- [ ] `singleton`
- [ ] `requiredVersion`
- [ ] `strictVersion`
- [ ] `remoteEntry.js`

Understand:

```text
Host
Remote
Exposed Module
Shared Dependency
Remote Entry
```

---



## 7. React + Micro Frontends

Know:

- [ ] React MFE architecture
- [ ] React Router integration
- [ ] Lazy loading
- [ ] Suspense
- [ ] Error boundaries
- [ ] Shared React instance
- [ ] Shared React DOM
- [ ] Context isolation
- [ ] State isolation
- [ ] Component sharing
- [ ] Hooks sharing
- [ ] Design system sharing
- [ ] TypeScript contracts
- [ ] Remote component loading

```text
React Shell
     |
     +---- React MFE: Customer
     |
     +---- React MFE: Orders
     |
     +---- React MFE: Reports
     |
     +---- React MFE: Admin
```

---



## 8. Routing

Know:

- [ ] Shell routing
- [ ] MFE routing
- [ ] Nested routing
- [ ] Route ownership
- [ ] URL contracts
- [ ] Deep linking
- [ ] Browser refresh
- [ ] 404 handling
- [ ] Authentication redirects
- [ ] Route-level lazy loading

Example:

```text
/app
   /customers      → Customer MFE
   /orders         → Order MFE
   /payments       → Payment MFE
   /reports        → Reporting MFE
```

Important question:

**Who owns the route?**

Establish clear route ownership rather than allowing multiple applications to manipulate the same route hierarchy unpredictably.

---



## 9. Communication Between MFEs

Know:

- [ ] Props
- [ ] Custom events
- [ ] Browser events
- [ ] Event bus
- [ ] Pub/Sub
- [ ] Shared state
- [ ] URL
- [ ] Web Storage
- [ ] Shared services
- [ ] API communication
- [ ] Backend communication
- [ ] `postMessage`
- [ ] Context
- [ ] RxJS/event streams



### Preferred principle

**Minimize direct communication between MFEs.**

Bad:

```text
MFE A → directly calls MFE B
MFE B → directly modifies MFE A state
```

Better:

```text
MFE A
 |
 Event
 |
 Event Bus
 |
 MFE B
```

---



## 10. State Management

Know:

- [ ] Local state
- [ ] MFE-local state
- [ ] Global state
- [ ] Shared state
- [ ] Redux
- [ ] Zustand
- [ ] Context
- [ ] Event-driven state
- [ ] URL state
- [ ] Server state
- [ ] React Query / TanStack Query



### Architect-level principle

```text
Local business state
        ↓
Keep inside MFE

Global application state
        ↓
Share carefully
```

Legitimate global state may include:

- Authentication
- User identity
- Tenant
- Locale
- Theme
- Feature flags

Avoid putting domain-specific business state into a giant global store without a strong architectural reason.

---



## 11. Shared Dependencies

Understand:

- [ ] React duplication
- [ ] React DOM duplication
- [ ] Library duplication
- [ ] Bundle size
- [ ] Singleton dependencies
- [ ] Version conflicts
- [ ] Compatibility
- [ ] Dependency governance

Example problem:

```text
MFE A → React 19
MFE B → React 18
MFE C → React 19
```

Questions:

- Which React version should be shared?
- What happens if versions are incompatible?
- What happens during rollout?
- Can different versions coexist?

---



## 12. Design System

Important for enterprise applications.

Know:

- [ ] Shared component library
- [ ] Design tokens
- [ ] Storybook
- [ ] CSS architecture
- [ ] Accessibility
- [ ] Versioning
- [ ] Breaking changes
- [ ] Component ownership
- [ ] Semantic versioning
- [ ] Visual regression testing

```text
                 Design System
                      |
          +-----------+-----------+
          |           |           |
        MFE A       MFE B       MFE C
```

Important distinction:

**Shared UI components are not necessarily Micro Frontends.**

A button library is a shared library, not an MFE.

---



## 13. CSS Isolation

Know:

- [ ] CSS collision
- [ ] Global CSS
- [ ] CSS Modules
- [ ] Shadow DOM
- [ ] CSS-in-JS
- [ ] Tailwind
- [ ] Naming conventions
- [ ] Design tokens
- [ ] Style isolation

Problem:

```text
MFE A:
.button { ... }

MFE B:
.button { ... }
```

Solutions:

- CSS Modules
- Shadow DOM
- Scoped styles
- BEM
- CSS-in-JS
- Utility classes with governance

---



## 14. Authentication & Authorization

Know:

- [ ] Authentication ownership
- [ ] OAuth 2.0
- [ ] OpenID Connect
- [ ] JWT
- [ ] Access tokens
- [ ] Refresh tokens
- [ ] SSO
- [ ] Session management
- [ ] RBAC
- [ ] ABAC
- [ ] Token propagation
- [ ] Token expiration
- [ ] Logout propagation

```text
                Identity Provider
                       |
                       ↓
                 Application Shell
                       |
             Authentication Context
                       |
          +------------+------------+
          |            |            |
        MFE A        MFE B        MFE C
```

---



## 15. Security

Know:

- [ ] XSS
- [ ] CSRF
- [ ] CSP
- [ ] CORS
- [ ] Subresource Integrity
- [ ] Trusted Types
- [ ] iframe security
- [ ] `postMessage` validation
- [ ] Token security
- [ ] Dependency vulnerabilities
- [ ] Remote JavaScript trust
- [ ] Supply-chain attacks



### Scenario

**What happens if a remote MFE is compromised?**

Discuss:

- Remote code is effectively trusted code.
- Strong CI/CD security is required.
- Dependency scanning.
- CSP where practical.
- SRI where applicable.
- Access controls.
- Isolation strategies.
- Monitoring.
- Deployment governance.
- Security reviews.

---



## 16. Performance

Know:

- [ ] Initial bundle size
- [ ] JavaScript duplication
- [ ] Lazy loading
- [ ] Code splitting
- [ ] Prefetching
- [ ] Preloading
- [ ] Caching
- [ ] CDN
- [ ] HTTP/2
- [ ] HTTP/3
- [ ] Compression
- [ ] Tree shaking
- [ ] Runtime overhead
- [ ] Network waterfall
- [ ] Core Web Vitals

Metrics:

- LCP
- INP
- CLS
- TTFB
- FCP

---



## 17. Failure Handling

Ask:

**What happens if one MFE goes down?**

```text
Shell
 |
 +---- MFE A ✓
 |
 +---- MFE B ✓
 |
 +---- MFE C ✗
          |
       Fallback
          |
     Error Boundary
```

Know:

- [ ] Error boundary
- [ ] Timeout
- [ ] Retry
- [ ] Fallback UI
- [ ] Circuit breaker concepts
- [ ] Remote unavailable
- [ ] Version mismatch
- [ ] Network failure
- [ ] Graceful degradation

---



## 18. Deployment

Fundamental reason for adopting MFE.

Know:

- [ ] Independent deployment
- [ ] CI/CD per MFE
- [ ] Versioning
- [ ] Rollback
- [ ] Blue/green deployment
- [ ] Canary deployment
- [ ] Feature flags
- [ ] CDN deployment
- [ ] Cache invalidation
- [ ] Artifact management

```text
Team A
  ↓
CI/CD
  ↓
Orders MFE
  ↓
CDN

Team B
  ↓
CI/CD
  ↓
Customer MFE
  ↓
CDN
```

---



## 19. Versioning

Understand:

- [ ] MFE versioning
- [ ] Semantic versioning
- [ ] API compatibility
- [ ] Contract compatibility
- [ ] Backward compatibility
- [ ] Breaking changes
- [ ] Remote version management
- [ ] Rollback compatibility



### Principle

A remote should not break the host because of an incompatible deployment.

---



## 20. CI/CD

Know how to build pipelines:

```text
Developer
   ↓
Git
   ↓
Build
   ↓
Unit Tests
   ↓
Lint
   ↓
Security Scan
   ↓
Integration Tests
   ↓
Contract Tests
   ↓
Build Artifact
   ↓
Deploy
   ↓
Smoke Test
   ↓
Production
```

---



## 21. Testing Strategy



### Unit

- [ ] Component tests
- [ ] Business logic tests
- [ ] Hook tests



### Integration

- [ ] MFE integration
- [ ] Shell integration
- [ ] Routing integration



### Contract

- [ ] Host/remote contracts
- [ ] API contracts
- [ ] Shared event contracts



### E2E

- [ ] Cypress
- [ ] Playwright



### Visual

- [ ] Storybook
- [ ] Visual regression



### Performance

- [ ] Lighthouse
- [ ] WebPageTest
- [ ] Real User Monitoring

---



## 22. Observability

Very important at enterprise scale.

Know:

- [ ] Logging
- [ ] Metrics
- [ ] Tracing
- [ ] Error tracking
- [ ] RUM
- [ ] Performance monitoring
- [ ] Correlation IDs
- [ ] Distributed tracing
- [ ] MFE identification

Example:

```text
User
 ↓
Shell
 ↓
Orders MFE
 ↓
Orders API
 ↓
Database
```

You should be able to trace a user request across the complete flow.

---



## 23. SSR / Next.js Micro Frontends

If the company uses Next.js, prepare this topic.

Know:

- [ ] SSR
- [ ] SSG
- [ ] ISR
- [ ] Server Components
- [ ] Client Components
- [ ] Streaming
- [ ] Edge rendering
- [ ] Runtime composition
- [ ] SEO implications
- [ ] Hydration
- [ ] Cache invalidation

Potential architecture:

```text
Next.js Shell
      |
      +---- Domain MFE
      |
      +---- Domain MFE
      |
      +---- Domain MFE
```

Next.js introduces additional complexity around server rendering, routing, hydration, and runtime composition.

---



## 24. Web Components

Know:

- [ ] Custom Elements
- [ ] Shadow DOM
- [ ] HTML templates
- [ ] Framework independence
- [ ] React integration
- [ ] Angular integration
- [ ] Vue integration
- [ ] Browser compatibility

Useful when different frameworks need to coexist:

```text
React MFE
Angular MFE
Vue MFE
```

---



## 25. iframe Approach



### Advantages

- Strong isolation
- CSS isolation
- JS isolation
- Independent deployment
- Technology independence



### Disadvantages

- Communication complexity
- UX issues
- SEO limitations
- Accessibility complexity
- Performance overhead
- Authentication complexity
- URL/routing complexity



### Interview question

**Would you use iframe for Micro Frontends?**

Good answer:

> I would consider it when strong isolation or legacy application integration is more important than seamless integration, but for most modern enterprise applications I'd prefer runtime composition or Web Components depending on the requirements.

---



## 26. Micro Frontend vs Monorepo

They solve different problems.

```text
Monorepo
   ↓
Repository strategy

Micro Frontend
   ↓
Application architecture
```

You can have:

```text
Micro Frontends + Monorepo
```

or:

```text
Micro Frontends + Multiple repositories
```

---



## 27. Monorepo Architecture

Know:

- [ ] Nx
- [ ] Turborepo
- [ ] pnpm workspaces
- [ ] Shared packages
- [ ] Dependency graph
- [ ] Build caching
- [ ] Affected builds
- [ ] Team boundaries

Example:

```text
repo/
├── apps/
│   ├── shell/
│   ├── customer/
│   ├── orders/
│   └── payments/
│
└── packages/
    ├── ui/
    ├── auth/
    ├── eslint-config/
    └── types/
```

---



## 28. Repository Strategies



### Single repository

Pros:

- Easier dependency management
- Shared tooling
- Easier refactoring

Cons:

- Coupling
- Larger repository
- Potential deployment coupling



### Multiple repositories

Pros:

- Strong team autonomy
- Independent releases

Cons:

- Dependency management
- Governance complexity
- Duplicate tooling

---



## 29. Data Ownership

Avoid:

```text
MFE A
  ↓
Database A

MFE B
  ↓
Database A
```

Prefer clear domain ownership:

```text
Customer MFE → Customer APIs
Order MFE    → Order APIs
Payment MFE  → Payment APIs
```

---



## 30. API Architecture

Understand:

- [ ] API Gateway
- [ ] BFF
- [ ] Domain APIs
- [ ] REST
- [ ] GraphQL
- [ ] API versioning
- [ ] Authentication
- [ ] Rate limiting
- [ ] Error contracts

Potential architecture:

```text
                 Frontend
                    |
             Micro Frontends
                    |
                  BFF
                    |
        +-----------+-----------+
        |           |           |
     Customer     Order      Payment
       API          API         API
```

---



## 31. Shared Backend vs Shared Frontend State

Frontend sharing:

```text
Auth
Theme
Locale
Feature flags
```

Backend sharing:

```text
Customer ID
Order ID
Tenant ID
Business data
```

Do not confuse frontend state ownership with backend domain ownership.

---



## 32. Cross-MFE Event Design

Design an event contract:

```typescript
type OrderCreatedEvent = {
  type: "ORDER_CREATED";
  payload: {
    orderId: string;
    customerId: string;
  };
};
```

Know:

- [ ] Event naming
- [ ] Payload contract
- [ ] Versioning
- [ ] Backward compatibility
- [ ] Event ownership
- [ ] Event validation
- [ ] Error handling

---



## 33. Technology Independence

Theoretical benefit:

```text
MFE A → React
MFE B → Angular
MFE C → Vue
```

But ask:

**Should we actually do this?**

Usually, no—unless there is a strong reason.

Different frameworks create:

- Larger bundles
- More runtime complexity
- More skill requirements
- More testing complexity
- More design-system challenges



### Principle

Technology independence is an option, not a goal.

---



## 34. Governance

Enterprise MFE needs governance.

Define:

- [ ] Coding standards
- [ ] Dependency standards
- [ ] Security standards
- [ ] Accessibility standards
- [ ] Performance budgets
- [ ] Design system standards
- [ ] API contracts
- [ ] Event contracts
- [ ] Versioning policies
- [ ] Deployment standards
- [ ] Observability standards

---



## 35. Team Ownership

Ideal:

```text
Customer Team
      ↓
Customer MFE

Order Team
      ↓
Order MFE

Payment Team
      ↓
Payment MFE
```

The team should ideally own:

```text
UI
API
Tests
Deployment
Monitoring
```

This is the **you-build-it-you-own-it** model.

---



## 36. Common Anti-Patterns



### ❌ Too many MFEs

```text
20-page application
→ 50 MFEs
```

Creates unnecessary complexity.

### ❌ Shared global state everywhere

Creates hidden coupling.

### ❌ Shared database

Creates domain coupling.

### ❌ Shell becomes monolith

All business logic moves into Shell.

### ❌ Excessive shared libraries

Everything becomes tightly coupled.

### ❌ Synchronous dependencies

MFE A cannot work until MFE B loads.

### ❌ Framework mixing without reason

React + Angular + Vue + Svelte simply because it is possible.

### ❌ No ownership

Nobody owns the MFE.

### ❌ No contract testing

Remote changes break host.

---



## 37. When NOT to Use Micro Frontends

Do not use MFE simply because it is trendy.

Avoid it when:

- [ ] Small team
- [ ] Small application
- [ ] One deployment team
- [ ] Strongly coupled UI
- [ ] No independent release requirement
- [ ] No domain boundaries
- [ ] Low organizational complexity
- [ ] Performance requirements are extremely strict
- [ ] Application is unlikely to evolve independently

A modular monolith may be better.

---



## 38. Micro Frontend vs Modular Monolith


| Area                 | Modular Monolith   | Micro Frontend                          |
| -------------------- | ------------------ | --------------------------------------- |
| Deployment           | Usually together   | Independent                             |
| Repository           | Usually shared     | Shared or separate                      |
| Runtime              | Single application | Multiple independently delivered pieces |
| Team autonomy        | Medium             | High                                    |
| Complexity           | Lower              | Higher                                  |
| Performance          | Usually simpler    | More challenging                        |
| Governance           | Easier             | More difficult                          |
| Release independence | Low                | High                                    |


---



## 39. Architect-Level Tradeoffs



### Benefits

- Team autonomy
- Independent deployment
- Independent scaling
- Domain ownership
- Incremental modernization
- Reduced organizational bottlenecks
- Technology migration



### Costs

- Operational complexity
- Performance overhead
- Dependency management
- Testing complexity
- Versioning
- Security
- Observability
- UX consistency
- Governance

---



## 40. Incremental Migration

Common real-world question:

**How would you migrate a large React monolith to Micro Frontends?**

Good approach:

```text
Existing Monolith
       |
       ↓
Identify domains
       |
       ↓
Create Shell
       |
       ↓
Extract one domain
       |
       ↓
Deploy independently
       |
       ↓
Observe
       |
       ↓
Extract next domain
       |
       ↓
Gradually retire monolith
```

Do not rewrite everything at once.

---



## 41. Strangler Pattern

```text
                 Application
                     |
          +----------+----------+
          |                     |
      New MFE               Legacy UI
          |                     |
       New domain          Remaining domain
```

Gradually replace old functionality.

---



## 42. Runtime Dependency Failure

Scenario:

**RemoteEntry.js is unavailable. What happens?**

Discuss:

- Timeout
- Retry
- Error boundary
- Fallback
- Cached version
- Monitoring
- User-friendly error
- Feature flag
- Circuit-breaker-style protection

---



## 43. Remote Version Compatibility

Scenario:

```text
Host v10

Remote v5
Remote v6
```

If Remote v6 requires a different React version, discuss:

- Dependency negotiation
- Compatibility matrix
- Semantic versioning
- Shared dependency policy
- Canary releases
- Rollback
- Contract tests

---



## 44. Performance Scenario

Question:

**You have 10 MFEs and page load becomes slow. How do you fix it?**

Answer:

- Lazy load MFEs
- Route-based loading
- Share dependencies
- Reduce duplicate libraries
- CDN
- Compression
- Preload critical resources
- Prefetch likely next routes
- Reduce JavaScript
- Tree shaking
- Performance budgets
- Measure Core Web Vitals
- RUM

---



## 45. Security Scenario

Question:

**One remote is owned by another team. How do you trust it?**

Discuss:

```text
Source
 ↓
Code Review
 ↓
Security Scan
 ↓
Dependency Scan
 ↓
CI
 ↓
Artifact
 ↓
CDN
 ↓
Runtime
```

Also mention:

- CSP
- SRI where appropriate
- Secure headers
- Dependency governance
- Vulnerability scanning
- Access controls
- Audit logs

---



## 46. Accessibility

Know:

- [ ] WCAG
- [ ] Keyboard navigation
- [ ] Screen readers
- [ ] ARIA
- [ ] Focus management
- [ ] Modal behavior
- [ ] Color contrast
- [ ] Consistent accessibility across MFEs

The Shell and individual MFEs must cooperate.

---



## 47. SEO

Know:

- [ ] CSR limitations
- [ ] SSR
- [ ] SSG
- [ ] Metadata
- [ ] Canonical URLs
- [ ] Structured data
- [ ] Crawlability

Particularly important for:

- E-commerce
- Content sites
- Marketing websites

Less important for:

- Internal enterprise admin applications

---



## 48. Caching

Know:

- [ ] Browser caching
- [ ] CDN caching
- [ ] Cache-Control
- [ ] Immutable assets
- [ ] Content hashing
- [ ] Remote entry caching
- [ ] Cache invalidation
- [ ] Versioned assets

Potential issue:

```text
User receives old remoteEntry.js
```

Understand how to prevent stale deployments.

---



## 49. Network Architecture

Understand:

```text
Browser
   |
CDN
   |
Shell
   |
RemoteEntry
   |
Remote chunks
   |
API Gateway
   |
BFF
   |
Microservices
```

Be able to explain the complete request lifecycle.

---



## 50. Interview Questions You Should Absolutely Prepare



### Beginner

1. What is Micro Frontend?
2. Why do we need it?
3. What are its advantages?
4. What are its disadvantages?
5. Microservices vs Micro Frontends?
6. Monolith vs Micro Frontend?



### Intermediate

1. What is Module Federation?
2. What is Host?
3. What is Remote?
4. What is Remote Entry?
5. How do MFEs communicate?
6. How do you share dependencies?
7. How do you share React?
8. How do you manage state?
9. How do you manage routing?
10. How do you handle authentication?
11. How do you handle CSS isolation?
12. How do you handle errors?
13. How do you deploy MFEs independently?



### Senior

1. How would you identify MFE boundaries?
2. How would you migrate a monolith?
3. How would you prevent Shell from becoming a monolith?
4. How do you handle remote failure?
5. How do you handle version incompatibility?
6. How do you manage shared dependencies?
7. How do you manage cross-MFE communication?
8. How do you design event contracts?
9. How do you manage global state?
10. How do you ensure performance?
11. How do you ensure security?
12. How do you implement observability?
13. How do you implement CI/CD?
14. How do you perform rollback?
15. How do you implement canary deployments?
16. How do you test MFEs?



### Architect

1. When would you NOT use Micro Frontends?
2. How would you design an enterprise MFE platform?
3. How would you establish governance?
4. How do you align MFE boundaries with organizational boundaries?
5. How would you handle multiple frontend frameworks?
6. How would you design a common design system?
7. How would you handle SSR?
8. How would you handle Next.js?
9. How would you support 20+ MFEs?
10. How would you prevent dependency hell?
11. How would you maintain backward compatibility?
12. How would you design disaster recovery?
13. How would you monitor MFE health?
14. How would you measure whether MFE adoption is successful?
15. What would make you reject Micro Frontends as an architecture?

---



## 51. The 10 Topics to Prioritize

If you have limited preparation time, master these first:


| Priority | Topic                       |
| -------- | --------------------------- |
| 🔴 1     | Micro Frontend fundamentals |
| 🔴 2     | Module Federation           |
| 🔴 3     | Domain decomposition        |
| 🔴 4     | Application Shell           |
| 🔴 5     | MFE communication           |
| 🔴 6     | State management            |
| 🔴 7     | Deployment & CI/CD          |
| 🔴 8     | Performance                 |
| 🔴 9     | Security                    |
| 🔴 10    | Migration from monolith     |


Then go deeper into:

**Routing → Design System → Testing → Observability → SSR/Next.js → Versioning → Governance → Failure handling.**

---



## 52. Architecture You Should Be Able to Draw in an Interview

Practice drawing this without looking at notes:

```text
                         USERS
                           |
                           ↓
                    CDN / Edge Layer
                           |
                           ↓
                  APPLICATION SHELL
                  /       |        \
                 /        |         \
                ↓         ↓          ↓
          Customer MFE  Order MFE  Payment MFE
                |         |          |
                ↓         ↓          ↓
             Customer    Order     Payment
               BFF        BFF        BFF
                |         |          |
                ↓         ↓          ↓
            Microservices / APIs
                 \         |        /
                  \        |       /
                   ↓       ↓      ↓
                    Domain Data

     Cross-Cutting Platform Services
     ├── Authentication
     ├── Authorization
     ├── Feature Flags
     ├── Design System
     ├── Observability
     ├── Analytics
     ├── Logging
     └── Security
```



### Interview explanation checklist

Be able to answer:

- [ ] Why these boundaries?
- [ ] Who owns each domain?
- [ ] How are MFEs loaded?
- [ ] How do they communicate?
- [ ] How are dependencies shared?
- [ ] What happens if one fails?
- [ ] How are they deployed?
- [ ] How are they monitored?
- [ ] How do you roll back?
- [ ] How do you secure them?

---



# Final Senior Architect Mental Model

When answering any Micro Frontend question, think through these dimensions:

```text
                 MICRO FRONTENDS
                        |
    +-------------------+-------------------+
    |                   |                   |
 BUSINESS             TECHNICAL          OPERATIONS
    |                   |                   |
 Domain boundaries    Composition         CI/CD
 Team ownership       Module Federation   Deployment
 Ownership             Routing             Rollback
 Coupling              State               Monitoring
 Release autonomy      Dependencies        Governance
    |                   |                   |
    +-------------------+-------------------+
                        |
                  USER EXPERIENCE
                        |
             Performance / UX / A11y
```

The strongest architect answer is rarely just **"use Module Federation."**

Instead, explain:

> **Business boundary → ownership → composition strategy → communication contract → dependency strategy → security → performance → testing → deployment → observability → governance → failure handling → migration strategy.**

That is the mindset expected from a **Senior Front-End Architect / Principal Architect**.
