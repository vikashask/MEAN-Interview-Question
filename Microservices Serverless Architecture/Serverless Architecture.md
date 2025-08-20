# Serverless Architecture – Architect’s Guide (with Interview Prep)

## 1) What is Serverless?

**Serverless** offloads server provisioning/management to the cloud so you focus on code and events. Two pillars:

- **FaaS (Functions‑as‑a‑Service):** e.g., AWS Lambda, Azure Functions, Google Cloud Functions. Short‑lived, event‑driven units of compute.
- **BaaS (Backend‑as‑a‑Service):** managed services (auth, data, queues, streams, storage) like Cognito/Auth0, DynamoDB/Firestore/Cosmos DB, SQS/Pub/Sub/Service Bus, S3/Blob/Cloud Storage.

**Key traits:** event‑driven, auto‑scale to zero (usually), pay‑per‑use, managed ops (patching, autoscaling, HA) by the provider.

---

## 2) Typical Reference Architectures

### AWS

- **Ingress:** API Gateway (REST/WebSocket) or ALB
- **Compute:** Lambda, Step Functions (sagas/workflows)
- **Data:** DynamoDB, Aurora Serverless, S3
- **Async:** SQS (queue), SNS (pub/sub), EventBridge (event bus)
- **Real‑time/Streams:** Kinesis, DynamoDB Streams
- **Observability/Sec:** CloudWatch, X‑Ray, CloudTrail, IAM, Secrets Manager, KMS

### Azure

- **Ingress:** Azure API Management / Functions Proxies
- **Compute:** Azure Functions, Durable Functions
- **Data:** Cosmos DB, Azure SQL Serverless, Blob Storage
- **Async:** Service Bus, Event Grid, Event Hubs
- **Observability/Sec:** App Insights, Azure Monitor, Defender for Cloud, Key Vault

### Google Cloud

- **Ingress:** API Gateway / Cloud Endpoints
- **Compute:** Cloud Functions, Cloud Run (serverless containers), Workflows
- **Data:** Firestore/Datastore, Cloud SQL Serverless, GCS
- **Async:** Pub/Sub, Eventarc
- **Observability/Sec:** Cloud Logging/Monitoring/Trace, Secret Manager, IAM

> **Pattern staples:** API → Auth → Function/Workflow → (Queue/Event) → Function(s) → Data store → Notifications.

---

## 3) Core Patterns (with notes)

- **Sync API with async backends:** Front API Gateway responds quickly; long work is queued (SQS/Service Bus/Pub/Sub). Client polls or gets Webhook/WS notification.
- **Fan‑out/Fan‑in:** EventBridge/Event Grid/Eventarc triggers multiple functions; aggregate results with Step Functions/Durable Functions/Workflows.
- **Saga/Orchestration:** Use Step Functions/Durable Functions for business processes with compensations; prefer choreography for simple flows.
- **CQRS + Event Sourcing:** Append events to a stream; project read models via functions for query scale.
- **Strangler Fig:** Gradually offload endpoints from monolith to serverless.
- **Scheduled/CRON:** Cloud Scheduler/EventBridge rules → functions for periodic jobs.

---

## 4) Architectural Trade‑offs

- **Cold starts:** language/runtime, VPC attachment, package size affect latency. Use provisioned concurrency / min instances for hot starts.
- **State:** keep functions stateless; externalize session, workflow and cache (Redis/Memcache, Step/Durable state, DynamoDB/Firestore).
- **Idempotency:** required for at‑least‑once events. Use idempotency keys + conditional writes.
- **Throughput & Backpressure:** set concurrency limits, use DLQs, exponential backoff/retries, circuit breakers.
- **Networking:** VPC access increases cold start; use private endpoints, VPC connectors, and limit egress.
- **Latency budgets:** avoid chatty synchronous chains; prefer async fan‑out or aggregate calls.
- **Vendor lock‑in:** weigh portability vs. velocity; isolate provider specifics behind ports/adapters.
- **Cost:** beware of chatty micro‑invocations, high request volumes, and per‑request auth; batch and cache.

---

## 5) Best Practices (Architect Level)

1. **Design for events first** (define canonical events and schemas; version them).
2. **Use asynchronous boundaries** to decouple and smooth spikes.
3. **Apply idempotency** at handlers and DB writes (conditional writes, upserts).
4. **Control concurrency**: set reserved/provisioned concurrency; prevent thundering herds.
5. **Batching & streaming**: process records in batches where possible; choose streaming (Kinesis/Hubs) for high TPS.
6. **Observability by default**: structured logs with correlation IDs; trace context propagation; RED/USE metrics.
7. **Security first**: least‑privilege IAM, short‑lived tokens, rotate secrets, encrypt at rest + in transit, private networking.
8. **API Gateway as policy point**: rate limiting, authN/Z, schema validation.
9. **Testing strategy**: contract tests for events/APIs; local emulators; integration tests against cloud in CI using sandbox accounts.
10. **Data modeling**: fit‑for‑purpose (NoSQL for hot paths; analytical sinks to lake/warehouse via events). Avoid cross‑service joins.
11. **Workflow resilience**: retries + timeouts + DLQs; compensating actions; explicit timeouts per step.
12. **Cost governance**: budgets, anomaly alerts, cost allocation tags, load tests to estimate $/txn; cache where it’s cheaper.
13. **Infrastructure‑as‑Code**: use CDK/Terraform/Serverless Framework; enforce reviews and policy‑as‑code (OPA/Conftest).
14. **Multi‑region/DR**: active/passive with async data replication; design for eventual consistency.
15. **Runtime choices**: prefer faster cold‑start runtimes (Node.js, Go); keep deps light; layer shared libs.

---

## 6) Interview Q&A – Intermediate

### Q1. Explain cold start and how to mitigate it.

**A:** Cold start is the latency when the platform needs to initialize runtime/containers. Mitigation: provisioned concurrency/min instances, lighter runtimes, smaller packages, avoid VPC when not needed, keep functions warm via traffic, and reuse connections (DB/http clients) outside handler.

### Q2. How do you handle long‑running processes?

**A:** Break into steps orchestrated by Step Functions/Durable Functions/Workflows. For >15 min compute or custom deps, use **serverless containers** (Cloud Run/Fargate) or batch services. Communicate progress via events/webhooks.

### Q3. When do you choose Cloud Run/Functions vs. Kubernetes?

**A:** Prefer serverless for event‑driven, bursty, stateless workloads with minimal ops. Choose K8s for long‑running services, custom networking, sidecars, or when you need full control and predictable latency/cost.

### Q4. How to design idempotent event handlers?

**A:** Include an idempotency key (message ID) and store a processed ledger; use conditional writes/transactions; ensure handlers are retry‑safe and order‑tolerant.

### Q5. How do you test serverless systems locally?

**A:** Use emulators (LocalStack/Azurite/Firestore emulator), contract tests for APIs/events, and minimal unit tests per handler. Still perform cloud integration tests in CI for parity.

---

## 7) Interview Q&A – Experienced

### Q1. Describe a production‑grade eventing strategy across domains.

**A:** Define domain events with versioned schemas (e.g., Avro/JSON Schema). Use a central event bus (EventBridge/Event Grid/Eventarc) with filtering and routing. Enforce schema compatibility checks in CI. Implement DLQs, retries, and observability on the bus; partition by keys for ordering where required.

### Q2. Design a multi‑region active/passive serverless system.

**A:** Read‑local/write‑global with conflict‑free IDs; replicate via streams; failover DNS (Route 53/Traffic Manager/Cloud DNS). Keep state in multi‑region DBs (DynamoDB global tables/Cosmos DB multi‑master/Firestore multi‑region). Ensure idempotent replay and regional feature flags.

### Q3. Control blast radius and cost for a runaway event storm.

**A:** Constrain concurrency per consumer, quotas, and rate limits at API Gateway/Event bus. Introduce token buckets and shard‑aware consumers. Auto‑pause non‑critical consumers, apply back‑pressure and DLQs, and add anomaly alerts.

### Q4. Secure inter‑service communication end‑to‑end.

**A:** mTLS or signed requests, private service endpoints/VPC links, least‑privilege IAM, short‑lived credentials (STS/Workload Identity), rotate secrets via managed vaults; validate JWTs at the edge.

### Q5. Migrating a monolith to serverless—stepwise approach?

**A:** Identify hot paths, carve out read‑heavy endpoints first (caching + API Gateway + Lambda). Use strangler fig via routing rules. Introduce events around key transactions; build new features on serverless while shrinking the monolith. Keep a shared auth/session until fully decomposed.

---

## 8) Hands‑on Preparation Plan (Architect)

**Week 1 – Foundations**

- Build a CRUD API with API Gateway/Functions + Serverless DB; add Auth (Cognito/Identity Platform/B2C).
- Add async queue + DLQ, implement idempotency and retries.

**Week 2 – Observability & Cost**

- Instrument traces/logs/metrics; build dashboards and SLOs.
- Run load tests; calculate cost per 1k requests; add caching and compare cost/latency.

**Week 3 – Workflows & DR**

- Orchestrate a 5‑step order pipeline with compensations.
- Add multi‑region simulation; failover test; verify replay idempotency.

**Interview Drills**

- Whiteboard 3 reference diagrams (API‑first, event‑first, stream processing).
- Prepare 5 war stories: cold‑start fix, cost runaway, DLQ replay, multi‑region failover, idempotency bug.
- Create a one‑pager on **build vs. lock‑in trade‑off** for leadership discussions.

---

## 9) Quick Checklists

**Design:** events, contracts, idempotency, concurrency limits, DLQ, cost model.  
**Security:** least‑privilege IAM, secrets, private networking, encryption, policy‑as‑code.  
**Ops:** dashboards, alerts, runbooks, chaos days, IaC, blue/green or canary.
