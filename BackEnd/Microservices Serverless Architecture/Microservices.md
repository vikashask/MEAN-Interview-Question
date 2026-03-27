# Microservices Interview Q&A

## Intermediate Level Questions

### 1. What are the main advantages of microservices over monolithic architecture?

**Answer:**

- Independent deployment of services
- Technology flexibility (different stacks per service)
- Scalability at the service level
- Fault isolation (failure in one service doesn’t bring down the entire system)
- Easier CI/CD pipelines for small teams

---

### 2. How do microservices communicate with each other?

**Answer:**

- **Synchronous:** REST, gRPC
- **Asynchronous:** Messaging queues like RabbitMQ, Kafka
- Choice depends on latency, throughput, and reliability requirements. Best practice: prefer async messaging for decoupling and resilience.

---

### 3. What are common challenges in microservices?

**Answer:**

- Distributed data management
- Network latency & reliability
- Monitoring & debugging across services
- Security and authentication between services
- Versioning APIs

---

### 4. What is service discovery and why is it important?

**Answer:**  
Service discovery allows services to dynamically locate each other without hard-coded endpoints. Tools like **Eureka, Consul, Kubernetes DNS** enable automatic registration and discovery. It ensures scalability and resilience.

---

### 5. How would you implement centralized logging in microservices?

**Answer:**  
Aggregate logs using tools like **ELK Stack (Elasticsearch, Logstash, Kibana)**, **Fluentd**, or **Splunk**. Use correlation IDs across service calls to trace requests. Best practice: make logs structured (JSON) and include metadata like request ID, timestamp, and service name.

---

## Experienced Level Questions

### 1. How do you handle data consistency across microservices?

**Answer:**

- Avoid distributed transactions (2PC).
- Use **Saga pattern** (choreography or orchestration).
- Implement **event sourcing** and **CQRS** for eventual consistency.
- Ensure idempotency in event handlers.

---

### 2. How do you secure microservices?

**Answer:**

- Use OAuth2 / OpenID Connect for authentication (via Identity Provider).
- Secure inter-service calls with mTLS.
- Apply **zero-trust principles** (each call must be authenticated/authorized).
- Limit exposure via API Gateway with rate limiting, throttling, and WAF integration.

---

### 3. How do you ensure observability in a microservices ecosystem?

**Answer:**

- **Logging:** Centralized, structured with correlation IDs.
- **Metrics:** Prometheus, Grafana dashboards for SLAs/SLOs.
- **Tracing:** Distributed tracing with OpenTelemetry, Jaeger, or Zipkin.
- **Health checks:** Liveness/readiness endpoints for orchestration tools.

---

### 4. How do you design fault tolerance in microservices?

**Answer:**

- Use retries with exponential backoff.
- Circuit breakers (Resilience4j, Hystrix).
- Bulkheads and rate limiting to prevent cascading failures.
- Deploy across multiple zones/regions for high availability.

---

### 5. What are best practices for designing microservices boundaries?

**Answer:**

- Align services with **business capabilities** (bounded context in DDD).
- Avoid creating distributed monoliths.
- Keep services loosely coupled but highly cohesive.
- Define clear API contracts with versioning.

---

### 6. How do you manage deployment of multiple microservices?

**Answer:**

- Use **containerization** (Docker) and **orchestration** (Kubernetes).
- Implement CI/CD pipelines with automated tests and canary/blue-green deployments.
- Apply Infrastructure as Code (Terraform, Helm) for reproducibility.

---
