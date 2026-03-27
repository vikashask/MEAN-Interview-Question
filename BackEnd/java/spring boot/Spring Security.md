# Spring Boot Security – Interview Q&A + Best Practices (Architect/Experienced)

## A. Core Interview Q&A (Intermediate → Experienced)

### 1) How do you configure Spring Security in Spring Boot 3+ without `WebSecurityConfigurerAdapter`?

**Answer:**  
Define a `SecurityFilterChain` bean and (optionally) a `PasswordEncoder`. Example:

```java
@Bean
SecurityFilterChain security(HttpSecurity http) throws Exception {
  http
    .csrf(csrf -> csrf.disable()) // enable for browser apps; disable for stateless APIs
    .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
    .authorizeHttpRequests(auth -> auth
        .requestMatchers("/actuator/health","/public/**").permitAll()
        .anyRequest().authenticated())
    .oauth2ResourceServer(oauth2 -> oauth2.jwt());
  return http.build();
}

@Bean PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(); }
```

---

### 2) When should you enable/disable CSRF in Spring Boot?

**Answer:**

- **Enable** CSRF for **stateful browser apps** using cookies/sessions to protect against cross‑site request forgery.
- **Disable** for **stateless token‑based APIs** (JWT) where the client sends `Authorization: Bearer` and no session cookies are involved. If you have a mixed app, keep CSRF enabled for form endpoints and exempt API routes.

---

### 3) How do you secure a REST API with OAuth2/JWT (Resource Server)?

**Answer:**  
Add `spring-boot-starter-oauth2-resource-server` and configure the issuer or JWK set:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/plant
          # or jwk-set-uri: https://auth.example.com/realms/plant/protocol/openid-connect/certs
```

Validate claims (aud, iss), set scopes to authorities, and use method security annotations like `@PreAuthorize("hasAuthority('SCOPE_bom.read')")`.

---

### 4) How do you add method-level authorization correctly in Spring Boot 3?

**Answer:**  
Enable method security and declare fine‑grained rules:

```java
@EnableMethodSecurity
@Configuration
class MethodSecurityConfig {}

@Service
class WorkOrderService {
  @PreAuthorize("hasAuthority('SCOPE_wo.read') or hasRole('SUPERVISOR')")
  public WorkOrder get(String id) { /* ... */ }
}
```

Prefer **authority checks** for scopes and **roles** for app RBAC; avoid mixing domain logic inside SpEL.

---

### 5) What is the correct way to store user passwords?

**Answer:**  
Always store **hashed** passwords using adaptive algorithms like **BCrypt/Argon2/PBKDF2** with a per‑user salt and strong work factor. Never store plain text or reversible encryption. Example:

```java
@Bean PasswordEncoder encoder() { return new BCryptPasswordEncoder(12); }
```

Rotate the cost factor based on performance testing.

---

### 6) How do you implement CORS safely in Spring Boot?

**Answer:**  
Configure explicit origins, methods, and headers. Avoid `*` in production for credentials.

```java
@Bean
CorsConfigurationSource cors() {
  CorsConfiguration cfg = new CorsConfiguration();
  cfg.setAllowedOrigins(List.of("https://app.example.com"));
  cfg.setAllowedMethods(List.of("GET","POST","PUT","DELETE"));
  cfg.setAllowedHeaders(List.of("Authorization","Content-Type"));
  cfg.setAllowCredentials(true);
  UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
  src.registerCorsConfiguration("/**", cfg);
  return src;
}
```

---

### 7) How do you secure Actuator endpoints?

**Answer:**  
Expose only required endpoints and restrict them:

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
```

```java
http.authorizeHttpRequests(a -> a
   .requestMatchers("/actuator/health","/actuator/info").permitAll()
   .requestMatchers("/actuator/**").hasRole("ADMIN")
);
```

Use network policies (K8s), mTLS, or a private ingress for sensitive endpoints.

---

### 8) How do you validate JWTs beyond signature verification?

**Answer:**  
Check **expiry (exp)**, **issuer (iss)**, **audience (aud)**, **not‑before (nbf)**, and **scope/roles**. Enforce token lifetimes and clock skew. Example converter:

```java
@Bean
JwtAuthenticationConverter jwtAuthConverter() {
  var converter = new JwtGrantedAuthoritiesConverter();
  converter.setAuthoritiesClaimName("scope");
  converter.setAuthorityPrefix("SCOPE_");
  var jwtConverter = new JwtAuthenticationConverter();
  jwtConverter.setJwtGrantedAuthoritiesConverter(converter);
  return jwtConverter;
}
```

Wire into `oauth2ResourceServer().jwt().jwtAuthenticationConverter(jwtAuthConverter())`.

---

### 9) What’s a robust approach for refresh tokens with JWT access tokens?

**Answer:**  
Use **short‑lived access tokens** (5–15 min) + **rotating refresh tokens** stored server‑side (or in an IdP) with **reuse detection**. Invalidate on rotation failure; bind refresh tokens to client, IP/device, and add **PKCE** for public clients.

---

### 10) How do you add mTLS between services?

**Answer:**  
Terminate TLS mutually at the gateway/ingress or between services using a service mesh (Istio/Linkerd). In Spring, configure the client with a key store and trust store (JKS/PKCS12) and the server with a trust store, setting `server.ssl.client-auth=need`.

---

### 11) How do you protect against common web attacks in Boot apps?

**Answer:**

- **XSS:** output encoding, CSP headers, sanitize inputs.
- **Clickjacking:** `X-Frame-Options: DENY` or `frame-ancestors` in CSP.
- **Open Redirects:** validate redirect targets.
- **SQLi:** use parameterized queries/JPA.
- **Mass assignment:** use DTOs and explicit mapping.

---

### 12) What’s the strategy for multi‑tenant authorization?

**Answer:**  
Include **tenantId** claim in JWT; enforce row‑level filtering at the repository level and in service methods. Use a `TenantContext` from the security context and add global filters (`@EntityGraph`/`@Where`, DB policies) to prevent cross‑tenant access.

---

## B. Best Practices Checklist (Apply in Production)

1. **Principle of Least Privilege:** narrow `@PreAuthorize` rules; lock down `actuator` and admin routes.
2. **Stateless APIs:** prefer Bearer JWT, `SESSION` disabled; keep cookies `HttpOnly`, `Secure`, `SameSite=Strict/Lax` when sessions are required.
3. **Strong Password Storage:** BCrypt/Argon2 with cost factor; never log passwords or tokens.
4. **Token Hygiene:** short‑lived access tokens, rotating refresh tokens, audience/issuer checks, clock skew, revoke on logout.
5. **Secrets Management:** use Vault/Cloud KMS/Secrets Manager; avoid secrets in `application.yml`; mount via env/volumes.
6. **Security Headers:** CSP, HSTS, X‑Content‑Type‑Options, Referrer‑Policy. Use a filter to apply globally.
7. **CORS:** explicit origins, no wildcard with credentials, preflight caching.
8. **Input Validation:** Bean Validation (JSR‑380) on DTOs; size limits for uploads/JSON.
9. **Rate Limiting/Brute Force:** gateway rate limits; captcha/slowdown on login; account lockout with care.
10. **mTLS / Network Segmentation:** private services; restrict egress/ingress; WAF at the edge.
11. **Observability:** trace IDs in logs, security audit logs, anomaly alerts for auth failures.
12. **Supply Chain:** pin dependencies, use OWASP Dependency-Check/Snyk; enable Spring’s AOT where applicable.
13. **Testing:** security slice tests, method‑security tests, integration tests with a real IdP (Keycloak/Auth0) in CI.
14. **Actuator Hardening:** expose minimal endpoints; protect `/env`/`/beans`; avoid exposing secrets in `/info`.
15. **Data Protection:** encrypt PII at rest, field‑level encryption if needed; tokenization for sensitive IDs.
16. **Access Reviews:** periodic role/scope audits; remove dormant accounts/clients.
17. **Error Handling:** avoid leaking details; return generic messages; trace with correlation IDs.
18. **Upgrades:** stay current with Spring Boot/Security CVEs and JDK updates.

---

## C. Quick Templates

**Security headers filter:**

```java
@Component
class SecurityHeadersFilter implements Filter {
  @Override public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
      throws IOException, ServletException {
    HttpServletResponse r = (HttpServletResponse) res;
    r.setHeader("X-Content-Type-Options", "nosniff");
    r.setHeader("X-Frame-Options", "DENY");
    r.setHeader("Referrer-Policy", "no-referrer");
    r.setHeader("Content-Security-Policy", "default-src 'self'");
    chain.doFilter(req, res);
  }
}
```

**Method security test skeleton:**

```java
@SpringBootTest
@AutoConfigureMockMvc
class WorkOrderSecurityTests {
  @Autowired MockMvc mvc;

  @Test
  void requiresAuth() throws Exception {
    mvc.perform(get("/workorders/1")).andExpect(status().isUnauthorized());
  }

  @WithMockUser(authorities = "SCOPE_wo.read")
  @Test
  void allowsScope() throws Exception {
    mvc.perform(get("/workorders/1")).andExpect(status().isOk());
  }
}
```

---

## D. How to Prepare for a Spring Security Interview (Architect)

1. **Hands‑on lab (half‑day):** build a small **OAuth2 Resource Server** with Keycloak or Auth0; secure 3 endpoints, add method security, and wire claims → authorities.
2. **Threat‑model walk‑through:** practice STRIDE on a sample Boot API; identify mitigations (headers, CSRF, rate limits, secrets).
3. **Whiteboard drills:** draw a login flow (Auth Code + PKCE), token validation path at the API, and refresh token rotation.
4. **War stories:** prepare 3–5 concise examples (e.g., JWT mis‑audience bug, CORS misconfig causing 401s, actuator leak, password hashing migration).
5. **Checklists:** memorize the Best Practices section above; keep a one‑pager for production hardening.

---

**Tip:** For mixed browser + API apps, consider **BFF (Backend‑for‑Frontend)** to keep tokens off the browser, maintain CSRF for the BFF only, and simplify CORS.
