# Spring Boot Essentials — Architect-Level Revision Guide

> For experienced developers (Node.js/Express, Python/Flask background). Not a textbook — a recall tool.

---

## 1. What Is Spring Boot?

**Spring** = massive Java framework ecosystem (DI, MVC, Data, Security, etc.).
**Spring Boot** = opinionated layer on top that auto-configures everything so you start coding in minutes.

| Aspect       | Spring (raw)                  | Spring Boot                        |
| ------------ | ----------------------------- | ---------------------------------- |
| Config       | Manual XML/Java config        | Convention over configuration      |
| Server       | Deploy WAR to external Tomcat | Embedded Tomcat/Jetty/Undertow     |
| Dependencies | You pick and match versions   | Starters with curated version sets |
| Startup      | Write boilerplate wiring      | `@SpringBootApplication` — done    |

### Framework Comparison

| Feature  | Express.js              | Flask               | Spring Boot                  |
| -------- | ----------------------- | ------------------- | ---------------------------- |
| Language | JavaScript/TS           | Python              | Java/Kotlin                  |
| Paradigm | Minimalist, middleware  | Micro-framework     | Full-featured, opinionated   |
| DI       | Manual / third-party    | Manual / extensions | Built-in IoC container       |
| ORM      | Mongoose / Prisma       | SQLAlchemy          | Spring Data JPA (Hibernate)  |
| Config   | `dotenv` / env vars     | `config.py` / env   | `application.yml` + profiles |
| Run      | `node app.js`           | `flask run`         | `mvn spring-boot:run`        |
| Package  | `node_modules` + source | `venv` + source     | Single fat JAR (`java -jar`) |

---

## 2. Project Setup

Go to [start.spring.io](https://start.spring.io), pick dependencies, download ZIP.

```
my-app/
  src/main/java/com/example/myapp/  # Code: controller/, service/, repository/, model/, dto/
      resources/application.yml      # Config (+ static/, templates/)
  src/test/java/com/example/myapp/  # Tests mirror main
  pom.xml                           # Maven (like package.json)
```

| Concept   | Node.js             | Maven                 | Gradle              |
| --------- | ------------------- | --------------------- | ------------------- |
| Manifest  | `package.json`      | `pom.xml`             | `build.gradle`      |
| Install   | `npm install`       | `mvn install`         | `./gradlew build`   |
| Run       | `npm start`         | `mvn spring-boot:run` | `./gradlew bootRun` |
| Lock file | `package-lock.json` | (managed by BOM)      | `gradle.lockfile`   |

```java
@SpringBootApplication
public class MyAppApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyAppApplication.class, args);
    }
}
// One class. One annotation. Server starts on port 8080.
```

---

## 3. Core Annotations (Daily Drivers)

| Annotation                | Purpose                                                                        | Quick Example                         |
| ------------------------- | ------------------------------------------------------------------------------ | ------------------------------------- |
| `@SpringBootApplication`  | Entry point = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan` | Main class                            |
| `@RestController`         | REST controller; JSON by default (= `@Controller` + `@ResponseBody`)           | API class                             |
| `@RequestMapping("/api")` | Base path for a controller                                                     | Class-level prefix                    |
| `@GetMapping("/{id}")`    | HTTP GET                                                                       | `findById(id)`                        |
| `@PostMapping`            | HTTP POST                                                                      | `create(dto)`                         |
| `@PutMapping("/{id}")`    | HTTP PUT                                                                       | `update(id, dto)`                     |
| `@DeleteMapping("/{id}")` | HTTP DELETE                                                                    | `delete(id)`                          |
| `@PathVariable`           | URL path: `/users/{id}`                                                        | `@PathVariable Long id`               |
| `@RequestParam`           | Query: `?status=ACTIVE`                                                        | `@RequestParam String status`         |
| `@RequestBody`            | Deserialize JSON body                                                          | `@RequestBody UserDTO dto`            |
| `@ResponseStatus`         | Set HTTP status                                                                | `@ResponseStatus(HttpStatus.CREATED)` |
| `@Valid`                  | Trigger bean validation                                                        | `@Valid @RequestBody dto`             |

### Express vs Spring Boot

```javascript
// Express
app.get("/api/users/:id", (req, res) => {
  res.json(userService.findById(req.params.id));
});
```

```java
// Spring Boot
@RestController @RequestMapping("/api/users")
public class UserController {
    private final UserService svc;
    UserController(UserService svc) { this.svc = svc; }
    @GetMapping("/{id}")
    public User findById(@PathVariable Long id) { return svc.findById(id); }
    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    public User create(@Valid @RequestBody UserDTO dto) { return svc.create(dto); }
}
```

---

## 4. Dependency Injection (DI)

Spring manages object creation and wiring via its IoC container. You declare what you need; the container provides it. Like a built-in "import and wire everything automatically" — no manual `require()` and `new`.

### Stereotype Annotations

| Annotation                        | Layer    | Purpose                               |
| --------------------------------- | -------- | ------------------------------------- |
| `@Component`                      | Generic  | Any Spring-managed bean               |
| `@Service`                        | Business | Service layer logic                   |
| `@Repository`                     | Data     | Data access; translates DB exceptions |
| `@Controller` / `@RestController` | Web      | HTTP request handling                 |

All four are functionally `@Component` — the difference is semantic clarity and layer-specific features.

### Injection Styles

```java
// PREFERRED: Constructor injection (immutable, testable)
@Service
public class OrderService {
    private final OrderRepository repo;
    private final NotificationService notifier;
    OrderService(OrderRepository repo, NotificationService notifier) { // auto-injected
        this.repo = repo; this.notifier = notifier;
    }
}
// Single constructor = @Autowired is optional (Spring infers it)

// AVOID: Field injection (hard to test, hides dependencies)
@Autowired private OrderRepository repo;
```

### Manual Bean Creation

```java
@Configuration
public class AppConfig {
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplateBuilder().setConnectTimeout(Duration.ofSeconds(5)).build();
    }
}
// Use @Bean in @Configuration for third-party classes you can't annotate with @Component.
```

### Bean Scopes

| Scope                 | Lifecycle                  | Use Case                      |
| --------------------- | -------------------------- | ----------------------------- |
| `singleton` (default) | One instance per container | Stateless services            |
| `prototype`           | New instance per injection | Stateful / non-shared objects |
| `request`             | One per HTTP request       | Request-scoped data           |
| `session`             | One per HTTP session       | User session data             |

### Resolving Ambiguity

```java
@Primary @Service class EmailNotifier implements Notifier { }  // default
@Service class SmsNotifier implements Notifier { }
// Or be explicit: OrderService(@Qualifier("smsNotifier") Notifier n) { ... }
```

---

## 5. Spring Data JPA

### Entity

```java
@Entity @Table(name = "products")
public class Product {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, length = 100)
    private String name;
    @Column(precision = 10, scale = 2)
    private BigDecimal price;
    @Enumerated(EnumType.STRING)
    private Status status;
    @CreationTimestamp
    private LocalDateTime createdAt;
}
```

### Repository (CRUD for Free)

```java
public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByStatus(Status status);                         // method name = query
    List<Product> findByNameContainingIgnoreCase(String keyword);
    Optional<Product> findByNameAndStatus(String name, Status status);

    @Query("SELECT p FROM Product p WHERE p.price > :min")             // JPQL
    List<Product> findExpensive(@Param("min") BigDecimal min);

    @Query(value = "SELECT * FROM products WHERE status = ?1", nativeQuery = true)
    List<Product> findByStatusNative(String status);
}
// Inherited: save(), findById(), findAll(), deleteById(), count() — zero implementation.
```

### Pagination

```java
@GetMapping
public Page<ProductDTO> list(Pageable pageable) { return svc.findAll(pageable); }
// GET /api/products?page=0&size=20&sort=name,asc
```

### DTOs — Never Expose Entities

`Client <--> DTO <--> Service <--> Entity <--> Database`

Map with MapStruct (compile-time) or ModelMapper (runtime). Exposing entities leaks internals and causes circular serialization.

### ORM Comparison

| Feature    | Mongoose (Node)    | SQLAlchemy (Python) | Spring Data JPA            |
| ---------- | ------------------ | ------------------- | -------------------------- |
| Schema     | Schema + Model     | Model class         | `@Entity` class            |
| Queries    | `.find({})`        | `session.query()`   | Method names / `@Query`    |
| Relations  | `ref` / `populate` | `relationship()`    | `@OneToMany`, `@ManyToOne` |
| Migrations | Manual             | Alembic             | Flyway / Liquibase         |
| Repository | Custom DAO         | Custom DAO          | `JpaRepository` (auto)     |

---

## 6. Configuration and Profiles

```yaml
server:
  port: 8080
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: ${DB_USER} # from env var
    password: ${DB_PASS}
  jpa:
    hibernate.ddl-auto: validate # never "create" in prod
app:
  feature:
    cache-enabled: true
    max-retries: 3
```

**Profiles:** `application.yml` (shared) + `application-dev.yml` + `application-prod.yml`.
Activate: `--spring.profiles.active=prod` or env `SPRING_PROFILES_ACTIVE=prod`.

### Injecting Config

```java
// Simple (fragile, no type safety)
@Value("${app.feature.max-retries:3}") private int maxRetries;

// PREFERRED: Type-safe config
@Validated @ConfigurationProperties(prefix = "app.feature")
public record FeatureProps(@NotNull Boolean cacheEnabled, @Min(1) int maxRetries) {}
// Enable: @EnableConfigurationProperties(FeatureProps.class) on any @Configuration
```

**Precedence (highest wins):** command-line args > OS env vars > `application-{profile}.yml` > `application.yml` > defaults.

**Secrets:** never in yml. Use env vars, HashiCorp Vault, AWS Secrets Manager, or K8s secrets.

---

## 7. Exception Handling

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        pd.setTitle("Resource Not Found");
        pd.setProperty("timestamp", Instant.now());
        return pd;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        ProblemDetail pd = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        pd.setTitle("Validation Failed");
        pd.setProperty("errors", ex.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(FieldError::getField, FieldError::getDefaultMessage)));
        return pd;
    }
}
```

```java
// Custom exception
@ResponseStatus(HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String resource, Object id) {
        super(resource + " not found with id: " + id);
    }
}
// throw new ResourceNotFoundException("Product", id);
```

`ProblemDetail` = Spring 6 built-in RFC 7807 support. Structured JSON: `type`, `title`, `status`, `detail`.

---

## 8. Validation

Add `spring-boot-starter-validation` (Hibernate Validator under the hood).

| Annotation                | Validates                                  |
| ------------------------- | ------------------------------------------ |
| `@NotNull`                | Not null (allows empty string)             |
| `@NotBlank`               | Not null, not empty, not whitespace        |
| `@NotEmpty`               | Not null, not empty (strings, collections) |
| `@Size(min, max)`         | String length or collection size           |
| `@Min(n)` / `@Max(n)`     | Numeric minimum / maximum                  |
| `@Email`                  | Email format                               |
| `@Pattern(regexp)`        | Regex match                                |
| `@Past` / `@Future`       | Date constraints                           |
| `@Positive` / `@Negative` | Number sign                                |

```java
// DTO with validation
public record CreateUserRequest(
    @NotBlank(message = "Name is required") String name,
    @Email(message = "Invalid email") String email,
    @Size(min = 8, max = 64, message = "Password: 8-64 chars") String password,
    @NotNull(message = "Role is required") Role role
) {}

// Controller: @Valid triggers it, errors caught by GlobalExceptionHandler (Section 7)
@PostMapping @ResponseStatus(HttpStatus.CREATED)
public UserDTO createUser(@Valid @RequestBody CreateUserRequest req) {
    return userService.create(req);
}
```

### Custom Validator

```java
@Target(ElementType.FIELD) @Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = NoProfanityValidator.class)
public @interface NoProfanity {
    String message() default "Contains prohibited words";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
public class NoProfanityValidator implements ConstraintValidator<NoProfanity, String> {
    public boolean isValid(String val, ConstraintValidatorContext ctx) {
        return val == null || !ProfanityFilter.containsBadWords(val);
    }
}
```

---

## 9. Starters

Curated dependency bundles. One line in `pom.xml` = full feature stack.

| Starter                                      | What It Brings                         |
| -------------------------------------------- | -------------------------------------- |
| `spring-boot-starter-web`                    | Spring MVC, Jackson, embedded Tomcat   |
| `spring-boot-starter-data-jpa`               | Hibernate, JPA, Spring Data repos      |
| `spring-boot-starter-security`               | Spring Security, filter chain, CSRF    |
| `spring-boot-starter-validation`             | Hibernate Validator (JSR-380)          |
| `spring-boot-starter-actuator`               | Health, metrics, Prometheus endpoints  |
| `spring-boot-starter-test`                   | JUnit 5, Mockito, MockMvc, AssertJ     |
| `spring-boot-starter-cache`                  | Caching abstraction (`@Cacheable`)     |
| `spring-boot-starter-webflux`                | Reactive web (Netty, WebClient)        |
| `spring-boot-starter-oauth2-resource-server` | JWT validation, OAuth2 resource server |

---

## 10. Actuator and Monitoring

| Endpoint               | Purpose                                       |
| ---------------------- | --------------------------------------------- |
| `/actuator/health`     | App health (UP/DOWN), DB, disk, custom checks |
| `/actuator/metrics`    | JVM, HTTP, custom metrics                     |
| `/actuator/info`       | Build info, git commit                        |
| `/actuator/env`        | Environment properties (mask secrets!)        |
| `/actuator/conditions` | Auto-configuration report                     |
| `/actuator/prometheus` | Prometheus-format metrics export              |

```yaml
management:
  endpoints.web.exposure.include: ["health", "info", "metrics", "prometheus"]
  endpoint.health:
    show-details: when-authorized
    probes.enabled: true # K8s liveness/readiness
    group.readiness.include: ["db", "diskSpace"]
```

```java
@Component
public class PaymentGatewayHealth extends AbstractHealthIndicator {
    @Override protected void doHealthCheck(Health.Builder b) {
        if (gateway.isReachable()) b.up().withDetail("latency", "45ms");
        else b.down().withDetail("error", "Connection refused");
    }
}
```

**Monitoring stack:** Actuator + Micrometer --> Prometheus --> Grafana.

---

## 11. Testing

| Annotation                       | Scope               | Loads               | Speed |
| -------------------------------- | ------------------- | ------------------- | ----- |
| `@SpringBootTest`                | Full integration    | Entire context      | Slow  |
| `@WebMvcTest(XController.class)` | Controller slice    | Web layer only      | Fast  |
| `@DataJpaTest`                   | Repository slice    | JPA + embedded DB   | Fast  |
| `@WebFluxTest`                   | Reactive controller | WebFlux layer       | Fast  |
| `@MockBean`                      | Mock a bean         | Replaces in context | --    |

### Controller Test

```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    @Autowired MockMvc mvc;
    @MockBean UserService userService;

    @Test void shouldReturnUser() throws Exception {
        when(userService.findById(1L)).thenReturn(new UserDTO(1L, "Alice", "a@b.com"));
        mvc.perform(get("/api/users/1"))
           .andExpect(status().isOk())
           .andExpect(jsonPath("$.name").value("Alice"));
    }
}
```

### Repository Test (Testcontainers)

```java
@DataJpaTest @Testcontainers
class ProductRepositoryTest {
    @Container static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16");
    @DynamicPropertySource static void props(DynamicPropertyRegistry r) {
        r.add("spring.datasource.url", pg::getJdbcUrl);
        r.add("spring.datasource.username", pg::getUsername);
        r.add("spring.datasource.password", pg::getPassword);
    }
    @Autowired ProductRepository repo;
    @Test void shouldFindByStatus() {
        repo.save(new Product(null, "Widget", BigDecimal.TEN, Status.ACTIVE, null));
        assertThat(repo.findByStatus(Status.ACTIVE)).hasSize(1);
    }
}
// Use Testcontainers for real DB tests. H2 hides dialect differences that break in prod.
```

---

## 12. Logging

Spring Boot uses **SLF4J + Logback** out of the box.

```java
private static final Logger log = LoggerFactory.getLogger(OrderService.class);
// or Lombok: @Slf4j on the class
log.info("Processing order for customer={}", req.customerId());
```

**Levels:** `ERROR > WARN > INFO > DEBUG > TRACE`

```yaml
logging:
  level:
    root: INFO
    com.example.myapp: DEBUG
    org.hibernate.SQL: DEBUG # show SQL queries
  structured.format: ecs # JSON in prod (Spring Boot 3.4+)
```

**MDC for correlation IDs:** `MDC.put("correlationId", UUID.randomUUID().toString())` in a filter. Every log line in that request carries it. Clean up with `MDC.clear()`.

---

## 13. API Versioning and Documentation

| Strategy  | Example            | Pros                       | Cons                   |
| --------- | ------------------ | -------------------------- | ---------------------- |
| URL path  | `/api/v1/users`    | Simple, visible, cacheable | URL pollution          |
| Header    | `X-API-Version: 2` | Clean URLs                 | Hidden, harder to test |
| Parameter | `?version=1`       | Flexible                   | Clutters query string  |

URL path is most common. Pick one and be consistent.

### OpenAPI with springdoc

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.8.0</version>
</dependency>
<!-- Swagger UI: http://localhost:8080/swagger-ui.html -->
```

```java
@Operation(summary = "Get user by ID")
@ApiResponse(responseCode = "200", description = "Found")
@ApiResponse(responseCode = "404", description = "Not found")
@GetMapping("/{id}")
public UserDTO findById(@Parameter(description = "User ID", example = "42") @PathVariable Long id) {
    return svc.findById(id);
}

// DTO documentation
public record UserDTO(
    @Schema(description = "Unique ID", example = "42") Long id,
    @Schema(description = "Full name", example = "Alice Smith") String name,
    @Schema(description = "Email", example = "alice@example.com") String email
) {}
```

---

## 14. Quick Recall

| #   | Concept                    | One-Liner                                                                            |
| --- | -------------------------- | ------------------------------------------------------------------------------------ |
| 1   | Boot vs Spring             | Boot = Spring + auto-config + embedded server + starters. Less XML, more coding.     |
| 2   | `@SpringBootApplication`   | = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`. Your main class. |
| 3   | Constructor injection      | Preferred DI. Immutable fields, no `@Autowired` needed with single constructor.      |
| 4   | `JpaRepository`            | Extend it, get CRUD + pagination + sorting. Method names become queries.             |
| 5   | Profiles                   | `application-{profile}.yml` + `SPRING_PROFILES_ACTIVE=prod`. Layer config per env.   |
| 6   | `@ConfigurationProperties` | Type-safe config with validation. Prefer over `@Value`.                              |
| 7   | `@RestControllerAdvice`    | Global exception handler. Pair with `@ExceptionHandler` for clean errors.            |
| 8   | `ProblemDetail`            | Spring 6 RFC 7807. Structured error JSON: `type`, `title`, `status`, `detail`.       |
| 9   | `@Valid` + DTOs            | Bean validation on input. Never trust the client. Never expose entities.             |
| 10  | Starters                   | One dependency = full stack. `starter-web`, `starter-data-jpa`, `starter-test`.      |
| 11  | Actuator                   | `/health`, `/metrics`, `/prometheus`. Expose minimally. Lock down with Security.     |
| 12  | `@WebMvcTest`              | Controller slice test. Fast. `@MockBean` for services. `MockMvc` for assertions.     |
| 13  | Testcontainers             | Real DB in tests via Docker. No H2 surprises. `@DynamicPropertySource` wires it.     |
| 14  | Structured logging         | SLF4J + Logback default. JSON in prod. MDC for correlation IDs.                      |
| 15  | springdoc-openapi          | Auto-generates Swagger UI + OpenAPI spec. `@Operation`, `@Schema`.                   |

_Consolidates spring-boot-interview.md, spring-java.md, validation dependency.md, Spring Security.md. See those for security deep-dives and manufacturing-domain examples._
