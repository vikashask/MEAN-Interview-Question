# Docker & Azure Container Registry (ACR)

> **Expert framing:** Writing *a* Dockerfile is basic; writing a **small, secure, cache-efficient, non-root, multi-stage** Dockerfile is expert. Also know the ACR authentication story cold — `admin-enabled false` + Managed Identity/AcrPull role is the production-correct answer, and interviewers specifically probe whether you'd reach for admin credentials (wrong) or RBAC (right).

## Why Containers?
Containers package your application + its dependencies into a single, portable unit that runs identically on any machine — your laptop, a CI server, or Azure.

```
Without containers:   "Works on my machine!" 😤
With containers:      "If it runs in the container, it runs everywhere." ✅
```

---

## Docker Core Concepts

```
Image    → A blueprint/template (immutable). Built from a Dockerfile.
Container → A running instance of an image.
Registry  → A storage service for images (Docker Hub, Azure Container Registry).
Layer     → Images are built in layers. Unchanged layers are cached.
```

---

## Writing a Production-Grade Dockerfile

### Node.js App (Multi-stage Build)
```dockerfile
# ==============================================
# Stage 1: BUILD (install dev dependencies)
# ==============================================
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package files first (better cache optimization)
COPY package*.json ./
RUN npm ci  # Deterministic install (uses package-lock.json)

# Copy source code
COPY . .
RUN npm run build  # e.g. TypeScript compilation or bundling

# ==============================================
# Stage 2: PRODUCTION (minimal final image)
# ==============================================
FROM node:20-alpine AS production

WORKDIR /app
ENV NODE_ENV=production

# Only copy production dependencies
COPY package*.json ./
RUN npm ci --omit=dev

# Copy built files from Stage 1
COPY --from=builder /app/dist ./dist

# Drop root privileges for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**Expert insight — why every line here earns its place:**
- **Multi-stage build**: the `builder` stage's dev dependencies, source TypeScript, and build tools never make it into the final image — only compiled output does. This is the single biggest lever for shrinking image size and attack surface, and interviewers use it as a quick "have you actually shipped containers to production" filter.
- **Copying `package*.json` before the rest of the source**: Docker caches layers; if only application code changed (not dependencies), this ordering means `npm ci` is served from cache instead of re-running — dramatically faster builds. Reversing this order (copying everything, then installing) busts the cache on every single code change.
- **`USER appuser` (non-root)**: running as root inside a container is a privilege-escalation risk if the container is ever compromised or escapes its sandbox — a container breakout as root can potentially affect the host. Non-root is a baseline security expectation in any production image review.
- **Pinning `node:20-alpine` instead of `node:latest`**: `latest` is a moving target — a rebuild next month could silently pull a different major Node version and break your app. Pin specific tags (ideally by digest for full immutability in high-security contexts).

### Key Dockerfile Instructions
```dockerfile
FROM node:20-alpine         # Base image (use specific tags, not 'latest')
WORKDIR /app                # Set working directory inside container
COPY src/ ./src/            # Copy files from host into container
RUN npm install             # Execute shell command during BUILD
ENV NODE_ENV=production     # Set environment variables
ARG BUILD_VERSION=1.0       # Build-time argument (not in final image)
EXPOSE 3000                 # Document which port the app listens on (metadata only)
CMD ["node", "server.js"]   # Command to run when container STARTS
ENTRYPOINT ["node"]         # Fixed command, CMD becomes its args
HEALTHCHECK --interval=30s CMD wget -qO- http://localhost:3000/health || exit 1
```

---

## Essential Docker Commands
```bash
# Build an image
docker build -t myapp:1.0 .
docker build -t myapp:1.0 --build-arg BUILD_VERSION=1.0 .

# List images
docker images

# Run a container
docker run -d \
  -p 8080:3000 \               # host_port:container_port
  -e DATABASE_URL="postgres://..." \  # Pass env vars
  --name myapp-container \
  myapp:1.0

# View running containers
docker ps

# View logs
docker logs myapp-container -f  # -f for follow/tail

# Open a shell inside a running container
docker exec -it myapp-container /bin/sh

# Stop and remove
docker stop myapp-container
docker rm myapp-container

# Build and run with Docker Compose
docker compose up --build -d
docker compose down
```

---

## Docker Compose (Local Multi-Container)
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://devuser:devpass@db:5432/appdb
    depends_on:
      - db
    volumes:
      - ./src:/app/src  # Live-reload for development

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

---

## Azure Container Registry (ACR)

### Create and Push to ACR
```bash
# Create ACR
az acr create \
  --resource-group rg-devops \
  --name mydevopsacr \
  --sku Basic \
  --admin-enabled false  # Prefer Managed Identities over admin credentials
# Expert note: the ACR "admin account" is a single shared username/password with
# full push/pull rights to the ENTIRE registry — no per-identity audit trail, no
# scoped permissions, and if it leaks, rotating it breaks every consumer at once.
# Production setups grant AcrPull/AcrPush RBAC roles to specific Managed
# Identities or Service Principals instead — individually revocable, auditable
# per-identity, and scoped to exactly what each consumer needs.

# Login to ACR (uses your az login credentials)
az acr login --name mydevopsacr

# Tag your local image with the ACR login server
docker tag myapp:1.0 mydevopsacr.azurecr.io/myapp:1.0

# Push the image
docker push mydevopsacr.azurecr.io/myapp:1.0

# List repositories in ACR
az acr repository list --name mydevopsacr --output table

# List tags for an image
az acr repository show-tags --name mydevopsacr --repository myapp
```

### Building and Pushing in Azure Pipelines
```yaml
# CI Pipeline: Build Docker image and push to ACR
- stage: Docker
  jobs:
    - job: BuildAndPush
      pool:
        vmImage: 'ubuntu-latest'
      steps:
        - task: Docker@2
          displayName: 'Build and Push to ACR'
          inputs:
            command: 'buildAndPush'
            repository: 'myapp'
            dockerfile: '$(System.DefaultWorkingDirectory)/Dockerfile'
            containerRegistry: 'MyACRServiceConnection'  # Service connection to ACR
            tags: |
              $(Build.BuildId)
              latest
```

---

## ACR Vulnerability Scanning
```bash
# Enable Microsoft Defender for Containers (scans images on push)
az acr update \
  --name mydevopsacr \
  --resource-group rg-devops \
  --anonymous-pull-enabled false

# View scan results for an image
az security sub-assessment list \
  --assessed-resource-id /subscriptions/<sub>/resourceGroups/rg-devops/providers/Microsoft.ContainerRegistry/registries/mydevopsacr
```

---

## Common Pitfalls & Expert Tips

- **Using `latest` tag in production deployments.** It's ambiguous which actual build is running, makes rollback guesswork, and breaks the immutability principle IaC/GitOps depends on. Tag images with something traceable — the build ID, git commit SHA, or semantic version.
- **Running containers as root** (skipping `USER` in the Dockerfile) — the single most common finding in container security reviews.
- **Not setting resource limits when running containers** — a container with a memory leak and no limit can starve the whole host, taking down unrelated workloads on the same machine.
- **Leaving the ACR admin account enabled "just in case."** It's a standing, broadly-scoped credential that undermines the whole point of using Managed Identities elsewhere — disable it and use RBAC (`AcrPull`/`AcrPush`) consistently.
- **Not scanning images for vulnerabilities before they reach production.** A clean build today can still contain a base-image OS package with a known CVE — continuous scanning (Defender for Containers or similar) catches vulnerabilities discovered *after* the image was built and pushed.
- **Bloated images from not using `.dockerignore`.** Without it, `COPY . .` pulls in `node_modules`, `.git`, and other junk into the build context, slowing builds and potentially leaking files (like `.env`) into the image.

---

## Practical Exercise ✅
1. Write a `Dockerfile` for a simple Node.js "Hello World" Express app (use multi-stage build).
2. Build the image locally and run it. Verify it responds at `http://localhost:3000`.
3. Create an ACR in Azure.
4. Tag and push the image to your ACR.
5. Automate this: Write a pipeline that builds and pushes to ACR on every commit to `main`.

---

## Expert Interview Q&A

**Q: Why use a multi-stage Dockerfile instead of just installing everything in one stage?**
A single-stage build bakes build tools, dev dependencies, and source artifacts (that are no longer needed at runtime) into the final image — increasing size and attack surface unnecessarily. Multi-stage builds let you use a full toolchain in an intermediate stage, then copy only the final compiled/production artifacts into a minimal final stage, producing a smaller, more secure runtime image.

**Q: Why is enabling the ACR admin account considered a security anti-pattern in production?**
It's a single shared credential with full registry access, has no per-consumer audit trail (you can't tell which service pulled which image), and rotating it (necessary if leaked) breaks every consumer simultaneously since they all share the same credential. RBAC-based access (Managed Identity or Service Principal granted `AcrPull`/`AcrPush`) gives per-identity, individually-revocable, auditable access instead.

**Q: A container is running fine in your Dockerfile locally but fails a security review for "running as root." Why does that matter if the app itself doesn't need special privileges?**
Container isolation (namespaces, cgroups) is not a perfect security boundary — a container escape vulnerability (in the runtime or kernel) run as root inside the container can translate to root-equivalent access on the host if exploited. Running as a non-root user inside the container limits the damage even if such an escape occurs — defense in depth, not a statement about whether the app itself needs elevated privileges.

**Q: How would you keep a production image up to date with security patches without changing your application code?**
Rebuild the image periodically (e.g., a scheduled pipeline) against the same base image tag so it pulls the latest patched layer, then push and redeploy — since Docker layers are content-addressed, a rebuild picks up upstream base-image security patches automatically. Pairing this with continuous vulnerability scanning (e.g., Defender for Containers) surfaces newly-discovered CVEs in already-deployed images so you know when a rebuild is actually needed.
