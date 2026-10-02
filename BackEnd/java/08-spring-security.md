# Spring Security — Architect-Level Revision Guide

> For experienced developers (Node.js / Python background). Not a textbook — a recall tool.

---

## 1. Mental Model

Security in Spring Boot is a **filter chain** — every HTTP request passes through an ordered list of filters before reaching your controller. You declare the rules; the framework enforces them.

```
Request --> Filter1 --> Filter2 --> ... --> FilterN --> Controller
               |            |                  |
          (CORS)      (AuthN: JWT?)      (AuthZ: roles?)
```

| Spring Security | Express Equivalent | Flask Equivalent |
|----------------|--------------------|------------------|
| `SecurityFilterChain` bean | `app.use(middleware)` chain | `@login_required` / Flask-Login |
| `@PreAuthorize` | Custom middleware per route | `@roles_required` decorator |
| `AuthenticationProvider` | Passport.js strategy | Flask-Security identity |
| Filters run in a defined order | Middleware runs in registration order | Decorators stack top-down |

**Core principle: secure by default.** Everything is locked down. You explicitly open what you need — the opposite of Express, where everything is open until you add auth middleware.

The `SecurityFilterChain` bean replaces all XML and adapter-based config. One bean = one set of rules.

---

## 2. Authentication vs Authorization

| Concept | Question | Example |
|---------|----------|---------|
| **Authentication (AuthN)** | "Who are you?" — verify identity | Login with username/password, present a JWT |
| **Authorization (AuthZ)** | "What can you do?" — check permissions | User has `ROLE_ADMIN`, scope `bom.read` |

AuthN always happens first. If AuthN fails, AuthZ is never reached.

---

## 3. Security Configuration (Spring Boot 3+)

`WebSecurityConfigurerAdapter` is **removed** since Spring Security 6 / Boot 3. All config is now bean-based.

### Complete Stateless JWT Setup

```java
@Configuration
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())                          // stateless API — no CSRF needed
            .sessionManagement(sm ->
                sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health", "/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
        return http.build();
    }

    @Bean
    PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(12); }
}
```

### CSRF Decision

| Scenario | CSRF | Why |
|----------|------|-----|
| Browser app with cookies/sessions | **Enable** (default) | Cookies are auto-sent; CSRF token prevents forgery |
| Stateless API with `Authorization: Bearer` | **Disable** | No cookies = no CSRF risk |
| Mixed (browser + API) | Enable for forms, exempt API paths | Use `csrf.ignoringRequestMatchers("/api/**")` |

### Session Policy

| Policy | When |
|--------|------|
| `STATELESS` | REST APIs with JWT — no `JSESSIONID` cookie |
| `IF_REQUIRED` | Traditional server-rendered apps (default) |
| `NEVER` | Don't create sessions but use them if they exist |

---

## 4. Authentication Methods

| Method | Use Case | How It Works |
|--------|----------|--------------|
| **In-memory** | Dev / testing | Hardcoded users in config — never production |
| **JDBC** | Simple apps | Users table in DB, `JdbcUserDetailsManager` |
| **LDAP** | Enterprise SSO | Binds to Active Directory / OpenLDAP |
| **OAuth2 / OIDC** | Modern APIs | Delegates to external IdP (Keycloak, Auth0, Okta) |
| **JWT** | Stateless APIs | Token-based, no server session, validated per request |
| **Custom** | Legacy systems | Implement `AuthenticationProvider` or `UserDetailsService` |

**OAuth2 vs JWT:** OAuth2 is the *protocol* (how tokens are issued). JWT is the *format* (how the token looks). You typically use both together — OAuth2 issues a JWT access token.

---

## 5. JWT Authentication (Deep Dive)

### Token Structure

```
header.payload.signature
  |        |        |
Base64   Base64   HMAC/RSA signed
(alg)   (claims)  (tamper-proof)
```

| Part | Contains |
|------|----------|
| **Header** | Algorithm (`RS256`), token type (`JWT`) |
| **Payload** | Claims: `sub`, `iss`, `aud`, `exp`, `iat`, custom (`roles`, `scope`) |
| **Signature** | `HMACSHA256(base64(header) + "." + base64(payload), secret)` |

### Access + Refresh Token Pattern

| Token | Lifetime | Storage | Purpose |
|-------|----------|---------|---------|
| **Access token** | 5-15 min | Memory / `Authorization` header | Authorize API requests |
| **Refresh token** | Hours-days | HttpOnly cookie or server-side | Get new access token without re-login |

Rotate refresh tokens on every use. Detect reuse = compromise = revoke entire family.

### Resource Server Setup

Add `spring-boot-starter-oauth2-resource-server`, then configure the issuer:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/myapp
          # OR specify the key set directly:
          # jwk-set-uri: https://auth.example.com/.well-known/jwks.json
```

Spring auto-fetches the public keys from the IdP, validates every incoming JWT, and populates the `SecurityContext`.

### JWT Validation Checklist

| Check | What | Fails If |
|-------|------|----------|
| **Signature** | Matches public key from JWKS | Token tampered or wrong key |
| **Expiry (`exp`)** | Not past current time (+ clock skew) | Token expired |
| **Issuer (`iss`)** | Matches expected issuer URI | Token from wrong IdP |
| **Audience (`aud`)** | Contains your service identifier | Token not meant for you |
| **Not Before (`nbf`)** | Current time is after `nbf` | Token used too early |
| **Scopes / Roles** | Has required permissions | Insufficient privileges |

### Mapping Claims to Spring Authorities

```java
@Bean
JwtAuthenticationConverter jwtAuthConverter() {
    var grantedAuthorities = new JwtGrantedAuthoritiesConverter();
    grantedAuthorities.setAuthoritiesClaimName("scope");
    grantedAuthorities.setAuthorityPrefix("SCOPE_");

    var converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(grantedAuthorities);
    return converter;
}
```

Wire it in: `.oauth2ResourceServer(o -> o.jwt(j -> j.jwtAuthenticationConverter(jwtAuthConverter())))`

---

## 6. Method-Level Security

Enable once, use everywhere:

```java
@EnableMethodSecurity   // on any @Configuration class
```

| Annotation | When It Runs | Example |
|-----------|--------------|---------|
| `@PreAuthorize` | **Before** method | `@PreAuthorize("hasRole('ADMIN')")` |
| `@PostAuthorize` | **After** method (can check return value) | `@PostAuthorize("returnObject.owner == principal.username")` |
| `@Secured` | Before method (simpler, no SpEL) | `@Secured("ROLE_USER")` |

### Common SpEL Expressions

| Expression | Meaning |
|-----------|---------|
| `hasRole('ADMIN')` | Has `ROLE_ADMIN` authority (prefix auto-added) |
| `hasAuthority('SCOPE_bom.read')` | Has exact authority string |
| `hasAnyRole('ADMIN','MANAGER')` | Has any of the listed roles |
| `principal.username` | Current user's username |
| `isAuthenticated()` | Any authenticated user |
| `permitAll()` | No restriction |
| `#id == principal.id` | Method param matches current user (param binding) |

```java
@Service
public class OrderService {
    @PreAuthorize("hasAuthority('SCOPE_order.read') or hasRole('SUPERVISOR')")
    public Order findById(String id) { /* ... */ }

    @PreAuthorize("#userId == principal.username or hasRole('ADMIN')")
    public List<Order> findByUser(String userId) { /* ... */ }
}
```

---

## 7. Password Storage

**Rule: NEVER store plaintext passwords.**

| Algorithm | Type | Notes |
|-----------|------|-------|
| **BCrypt** | Adaptive hash | Default choice. Built-in salt. Cost factor = 2^n iterations |
| **Argon2** | Memory-hard hash | Resistant to GPU attacks. Best for new systems |
| **PBKDF2** | Iterative hash | NIST approved. Slower than BCrypt on GPUs |
| **SCrypt** | Memory-hard hash | Middle ground between BCrypt and Argon2 |

```java
@Bean
PasswordEncoder encoder() {
    return new BCryptPasswordEncoder(12);  // cost factor 12 = 2^12 iterations
}
```

Cost factor tuning: target ~250ms per hash on your production hardware. Increase the factor as hardware gets faster. BCrypt default is 10; use 12+ for production.

`DelegatingPasswordEncoder` handles migration between algorithms by storing the algorithm prefix: `{bcrypt}$2a$12$...`

---

## 8. CORS Configuration

CORS works the same as in Express (`cors` middleware) — the browser blocks cross-origin requests unless the server explicitly allows them.

```java
@Bean
CorsConfigurationSource corsConfig() {
    CorsConfiguration cfg = new CorsConfiguration();
    cfg.setAllowedOrigins(List.of("https://app.example.com"));
    cfg.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    cfg.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    cfg.setAllowCredentials(true);
    cfg.setMaxAge(3600L);  // preflight cache: 1 hour

    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", cfg);
    return source;
}
```

| Rule | Why |
|------|-----|
| Explicit origins, never `*` with credentials | `*` + credentials = browser rejects the response |
| List only methods your API actually uses | Minimizes attack surface |
| Set `maxAge` for preflight caching | Reduces OPTIONS requests |
| Register as a bean, not in the filter chain | Spring Security picks it up automatically via `CorsConfigurationSource` |

---

## 9. Security Headers

Spring Security adds several headers by default. Key ones to know:

| Header | Value | Purpose | Default? |
|--------|-------|---------|----------|
| `X-Content-Type-Options` | `nosniff` | Prevents MIME-type sniffing | Yes |
| `X-Frame-Options` | `DENY` | Blocks clickjacking via iframes | Yes |
| `X-XSS-Protection` | `0` | Disables buggy browser XSS filter | Yes |
| `Strict-Transport-Security` | `max-age=31536000` | Forces HTTPS for 1 year | Yes (HTTPS only) |
| `Cache-Control` | `no-cache, no-store` | Prevents caching sensitive responses | Yes |
| `Content-Security-Policy` | `default-src 'self'` | Restricts resource loading origins | **No** — add manually |
| `Referrer-Policy` | `no-referrer` | Controls referrer header leaking | **No** — add manually |

### Custom Headers Filter

```java
@Component
class SecurityHeadersFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletResponse response = (HttpServletResponse) res;
        response.setHeader("Content-Security-Policy", "default-src 'self'");
        response.setHeader("Referrer-Policy", "no-referrer");
        chain.doFilter(req, res);
    }
}
```

Or configure in the `SecurityFilterChain`: `.headers(h -> h.contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'")))`

---

## 10. Actuator Security

Actuator exposes operational endpoints. In production, most must be locked down.

```yaml
management:
  endpoints:
    web:
      exposure:
        include: [ "health", "info", "metrics", "prometheus" ]
  endpoint:
    health:
      probes:
        enabled: true      # enables /health/liveness and /health/readiness
```

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/actuator/health", "/actuator/info").permitAll()
    .requestMatchers("/actuator/**").hasRole("ADMIN")
);
```

| Environment | Strategy |
|-------------|----------|
| Development | Expose all, no auth |
| Staging | Expose most, require auth |
| Production | Expose only health/info/metrics publicly. Lock `/env`, `/beans`, `/configprops` behind ADMIN. Use network policies (K8s `NetworkPolicy`, private ingress) to restrict access at the infrastructure level |

---

## 11. Common Attack Protection

| Attack | What Happens | Spring Boot Defense |
|--------|-------------|---------------------|
| **XSS** | Malicious script injected into page | Output encoding (Thymeleaf auto-escapes), CSP headers |
| **CSRF** | Forged requests using victim's cookies | CSRF tokens enabled by default for form-based apps |
| **SQL Injection** | Raw SQL injected via input | JPA parameterized queries, never string-concatenate SQL |
| **Clickjacking** | Page embedded in malicious iframe | `X-Frame-Options: DENY` (default header) |
| **Session Fixation** | Attacker sets victim's session ID | Session ID regenerated on authentication (default) |
| **Brute Force** | Repeated login attempts | Rate limiting at gateway, account lockout, CAPTCHA |
| **Open Redirect** | User redirected to malicious site | Validate redirect targets, whitelist allowed URLs |
| **Mass Assignment** | Extra fields bound to entity | Use DTOs with explicit field mapping, never bind to entities |

---

## 12. Production Checklist

1. `SecurityFilterChain` bean with explicit rules — no open-by-default endpoints
2. CSRF enabled for browser apps, disabled only for stateless APIs
3. Session policy `STATELESS` for JWT-based APIs
4. Passwords hashed with BCrypt (cost 12+) or Argon2 — never plaintext or MD5/SHA
5. Short-lived access tokens (5-15 min) + rotating refresh tokens with reuse detection
6. JWT validated: signature, expiry, issuer, audience, scopes
7. Method security (`@PreAuthorize`) on service methods, not just URL patterns
8. CORS: explicit origins, no wildcard with credentials
9. Security headers: CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`
10. Actuator: only health/info/metrics public; `/env`, `/beans` behind ADMIN + network restriction
11. Secrets in Vault / Cloud KMS / env vars — never in `application.yml` committed to Git
12. Input validation: Bean Validation (JSR-380) on all DTOs, size limits on uploads/JSON
13. Rate limiting at API gateway; account lockout with exponential backoff
14. Dependency scanning: OWASP Dependency-Check or Snyk in CI pipeline
15. Security tests: `@WithMockUser` unit tests, integration tests with real IdP in CI

---

## 13. Quick Recall

| # | Concept | One-Liner |
|---|---------|-----------|
| 1 | Filter chain | Security = ordered filter chain. `SecurityFilterChain` bean defines all rules. |
| 2 | Secure by default | Everything locked down. You `permitAll()` what you open. Opposite of Express. |
| 3 | AuthN vs AuthZ | AuthN = who are you (identity). AuthZ = what can you do (permissions). AuthN first. |
| 4 | No more adapter | `WebSecurityConfigurerAdapter` is removed. Bean-based config only in Boot 3+. |
| 5 | JWT validation | Check signature, expiry, issuer, audience, scopes. Auto-configured with `issuer-uri`. |
| 6 | Method security | `@EnableMethodSecurity` + `@PreAuthorize(SpEL)`. Prefer authority checks over role checks. |
| 7 | Password hashing | BCrypt(12+) or Argon2. Never plaintext. `DelegatingPasswordEncoder` handles migration. |
| 8 | CSRF rule | Enable for cookies/sessions. Disable for stateless Bearer token APIs. |
| 9 | CORS rule | Explicit origins. Never `*` with credentials. Cache preflight with `maxAge`. |
| 10 | Actuator | Expose only health/info/metrics. Lock the rest behind ADMIN + network policy. |
| 11 | Refresh tokens | Short access (5-15 min) + rotating refresh. Reuse detection = revoke family. |
| 12 | Attack defaults | Spring adds XSS, clickjacking, session-fixation protection out of the box. Add CSP manually. |

---

*Previous: [07 — Design Patterns](./07-design-patterns.md) | Next: [09 — Spring Boot & Microservices](./09-spring-boot-microservices.md)*
