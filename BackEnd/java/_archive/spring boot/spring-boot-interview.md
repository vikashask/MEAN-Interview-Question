# Spring Boot – Intermediate Level Interview Q&A

### 1) What are Spring Boot Starters and why are they useful?

**Answer:**  
Starters are curated dependency descriptors that simplify project setup. For example, `spring-boot-starter-web` pulls in Spring MVC, Jackson, validation, and Tomcat by default. They remove the need to manually manage compatible versions. This reduces boilerplate in `pom.xml`/`build.gradle` and ensures consistent dependencies.

---

### 2) How does Spring Boot manage profiles and environment properties?

**Answer:**  
Profiles (`@Profile`, `spring.profiles.active`) allow different beans and properties per environment (dev, test, prod). Configuration can come from `application.yml`, command-line args, OS env vars, or Spring Cloud Config. The property resolution follows a defined precedence (command line > OS env > application.yml). Profiles can be combined (e.g., `dev,aws`) for layered config.

---

### 3) How does Spring Boot embed servers and what are the benefits?

**Answer:**  
By default, Boot uses embedded servers like Tomcat, Jetty, or Undertow. The application is packaged as a JAR with the server, so it can run via `java -jar`. Benefits: no need for external servlet container installation, simpler deployment, and consistency between environments. You can switch servers by changing a starter dependency.

---

### 4) What is the difference between `@RestController` and `@Controller`?

**Answer:**  
`@Controller` marks a class as a web controller and returns views (e.g., Thymeleaf templates). To return JSON/XML, you need `@ResponseBody` on methods.  
`@RestController` is shorthand for `@Controller + @ResponseBody`, making it the default for REST APIs, automatically serializing objects to JSON/XML.

---

### 5) How does Spring Boot simplify error handling?

**Answer:**  
Spring Boot provides a default `/error` mapping with sensible error responses (JSON for REST). You can override with a `@ControllerAdvice` and `@ExceptionHandler` for global exception handling. You can also implement `ErrorController` for fully custom error responses. This reduces boilerplate for handling 404, 500, and custom exceptions.

---

### 6) What role does Spring Boot Actuator play for intermediate developers?

**Answer:**  
Actuator exposes runtime endpoints for monitoring and management (`/actuator/health`, `/metrics`, `/env`). Intermediate developers use it to understand application internals, integrate with monitoring systems, and debug configuration. It’s a bridge toward production readiness, even in development environments.

# Spring Boot – Experienced Level Interview Q&A

### 1) Explain Spring Boot auto-configuration. How do you customize or troubleshoot it?

**Answer:**  
Spring Boot uses `spring.factories`/`AutoConfiguration.imports` to conditionally create beans based on classpath, properties, and existing beans. Customize via:

- **Exclude:** `@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})` or `spring.autoconfigure.exclude`.
- **Order:** `@AutoConfiguration(before = …, after = …)`.
- **Conditional beans:** `@ConditionalOnMissingBean`, `@ConditionalOnClass`, `@ConditionalOnProperty`.
- **Troubleshoot:** Enable `debug=true` to print the **auto-configuration report**; use `actuator/conditions` endpoint to see why beans matched/missed.

---

### 2) `@Configuration(proxyBeanMethods = false)`—when and why?

**Answer:**  
By default, `@Configuration` classes are CGLIB-proxied (`proxyBeanMethods = true`) to preserve singleton semantics for `@Bean` methods that call each other. Setting `false` removes the proxy, improving startup time/AOT compatibility, but you must avoid inter-bean method calls that rely on proxying; otherwise multiple instances may be created.

---

### 3) How do you design resilient configuration management?

**Answer:**  
Use **type-safe configuration** with `@ConfigurationProperties` + JSR‑303 validation (`@Validated`). Externalize secrets to a vault (e.g., HashiCorp Vault, AWS Secrets Manager) and mount via Spring Cloud Config or environment variables. Support profiles (`application-prod.yml`) and immutable records for properties in Java 17+:

```java
@Validated
@ConfigurationProperties(prefix = "plant")
public record PlantProps(@NotBlank String name, @Min(1) int lines) {}
```

---

### 4) Observability in production (metrics, logs, traces)?

**Answer:**  
Use **Micrometer** to export to Prometheus/CloudWatch; add **OpenTelemetry** for distributed tracing. Propagate trace ids via `spring.sleuth` (or OTel instrumentation). Standardize logs in JSON with correlation ids. Create SLOs on critical endpoints and wire **Actuator** health groups with readiness/liveness for K8s probes.

---

### 5) Transaction boundaries across microservices (Saga vs. 2PC)?

**Answer:**  
Avoid 2PC; model **Sagas** with outbox pattern + idempotent consumers. Use a local ACID transaction to persist state and publish a domain event atomically (Debezium/outbox table). Compensating actions undo prior steps on failure. Ensure **exactly-once effect** through idempotency keys and **`@Transactional`** only within a service boundary.

---

### 6) Reactive vs. Servlet stack—how to choose?

**Answer:**  
Choose **WebFlux** for high‑concurrency I/O-bound workloads (e.g., streaming device data), and **Spring MVC** for CPU-bound or blocking dependencies. Don’t mix blocking JDBC calls in reactive code; use R2DBC or delegate blocking work to bounded schedulers. Measure with load tests before deciding.

---

### 7) Practical caching strategy in Spring Boot?

**Answer:**  
Enable with `@EnableCaching` and annotate methods with `@Cacheable`, `@CachePut`, `@CacheEvict`. Use Redis for distributed caching; set **TTL**, **cache keys**, and handle **cache stampede** (e.g., jittered TTL, background refresh). Example:

```java
@Cacheable(cacheNames = "bom", key = "#id")
public Bom getBom(long id) { return repo.findById(id).orElseThrow(); }
```

---

### 8) Secure a resource server with method-level rules

**Answer:**  
Configure OAuth2 Resource Server (JWT) and layer **`@PreAuthorize`** rules:

```java
@Bean SecurityFilterChain http(HttpSecurity h) throws Exception {
  h.oauth2ResourceServer(o -> o.jwt());
  h.authorizeHttpRequests(a -> a
      .requestMatchers("/actuator/**").hasRole("ADMIN")
      .anyRequest().authenticated());
  return h.build();
}
@Service
class WorkOrderService {
  @PreAuthorize("hasAuthority('SCOPE_wo.read')")
  public WorkOrder get(String id) { /*...*/ }
}
```

---

### 9) Database testing at experience level

**Answer:**  
Use **Testcontainers** for real DBs, not H2, to avoid prod‑parity gaps. Prefer slice tests (`@DataJpaTest`, `@WebMvcTest`) for speed and a few end‑to‑end tests with `SpringBootTest` + Testcontainers network. Keep migrations with **Flyway/Liquibase** and run them in tests.

---

### 10) Graceful shutdown & startup optimization

**Answer:**  
Enable graceful shutdown (`server.shutdown=graceful`) so in‑flight requests complete before pod termination. Reduce startup with lazy init, removing unused starters, `proxyBeanMethods=false`, and consider **AOT/native image** (GraalVM) for CLI/edge services.

---

### 11) Idempotent REST design

**Answer:**  
Use natural idempotency (PUT/DELETE) or **Idempotency-Key** headers for POST creating resources. Persist request keys with status to avoid duplicate effects on retries. Combine with **optimistic locking** (`@Version`).

---

### 12) Actuator in production—what to expose?

**Answer:**  
Expose only necessary endpoints (`health`, `info`, `metrics`, `prometheus`). Use health groups for readiness vs. liveness and restrict access via network policies and Spring Security. Example `application.yml`:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: ["health", "info", "metrics", "prometheus"]
  endpoint:
    health:
      probes:
        enabled: true
      group:
        readiness:
          include: ["db", "ping", "diskSpace"]
```

---
