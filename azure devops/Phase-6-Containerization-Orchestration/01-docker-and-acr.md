# Docker & Azure Container Registry (ACR)

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

## Practical Exercise ✅
1. Write a `Dockerfile` for a simple Node.js "Hello World" Express app (use multi-stage build).
2. Build the image locally and run it. Verify it responds at `http://localhost:3000`.
3. Create an ACR in Azure.
4. Tag and push the image to your ACR.
5. Automate this: Write a pipeline that builds and pushes to ACR on every commit to `main`.
