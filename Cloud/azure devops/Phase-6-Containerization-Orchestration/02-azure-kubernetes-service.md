# Azure Kubernetes Service (AKS)

> **Expert framing:** Deploying a YAML manifest is basic Kubernetes. Expert Kubernetes is knowing *why* `resources.requests/limits` and probes exist (cluster stability, not just best-practice boilerplate), understanding what actually happens during a rolling update when `maxUnavailable: 0`, and being able to debug a `CrashLoopBackOff` or a Pod stuck in `Pending` from first principles rather than just re-applying and hoping.

## Core Kubernetes Concepts

```
Node          → A VM running in your cluster.
Pod           → The smallest unit. Runs one or more containers. Ephemeral.
Deployment    → Manages Pods: handles rolling updates, restarts.
Service       → A stable network endpoint to access Pods (Pods have dynamic IPs).
ConfigMap     → Store non-secret config (env vars, config files).
Secret        → Store sensitive data (passwords, connection strings). Base64 encoded.
Ingress       → HTTP/HTTPS routing rules (sends /api/* to one service, /* to another).
Namespace     → Virtual cluster within a cluster (e.g., dev, staging namespaces).
```

---

## Creating an AKS Cluster

```bash
# Create a simple AKS cluster (not for production - no HA)
az aks create \
  --resource-group rg-devops \
  --name aks-myapp-dev \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --enable-managed-identity \
  --attach-acr mydevopsacr \   # Grant AKS access to pull from your ACR
  --generate-ssh-keys

# Download credentials (configure kubectl to talk to this cluster)
az aks get-credentials \
  --resource-group rg-devops \
  --name aks-myapp-dev

# Verify connection
kubectl get nodes
```

---

## Core Kubernetes YAML Manifests

### Deployment + Service
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  namespace: default
  labels:
    app: myapp
spec:
  replicas: 3                   # Run 3 copies of the Pod
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1               # At most 1 extra Pod during update
      maxUnavailable: 0         # Never kill a Pod before a new one is ready
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: mydevopsacr.azurecr.io/myapp:$(BUILD_ID)   # Filled in by pipeline
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_PASSWORD
              valueFrom:
                secretKeyRef:              # Reference a Kubernetes Secret
                  name: myapp-secrets
                  key: db-password
          resources:                       # VERY important for cluster stability
            requests:
              cpu: "100m"                  # 100 millicores = 0.1 CPU
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:                   # Restart container if this fails
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:                  # Only route traffic when this passes
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10

# Expert insight — these aren't boilerplate, they solve specific failure modes:
# - `resources.requests` is what the SCHEDULER uses to decide which node has
#   room for this Pod — no requests set means the scheduler can over-pack a
#   node, causing every Pod on it to compete for real resources under load.
# - `resources.limits` is what the KUBELET enforces at runtime — exceeding the
#   memory limit gets the container OOMKilled; exceeding CPU limit gets it
#   throttled (not killed). A container with no limits can starve its
#   neighbors on a shared node — this is the single most common cause of
#   "random unrelated Pods keep restarting" incidents.
# - `livenessProbe` failing restarts the CONTAINER (assumes it's stuck/dead).
# - `readinessProbe` failing removes the Pod from the SERVICE's endpoints
#   (traffic stops routing to it) WITHOUT restarting it — critical during
#   slow startup (DB connection warming up) so traffic doesn't hit a Pod
#   that's alive but not yet able to serve requests. Confusing liveness with
#   readiness is one of the most common AKS/K8s interview trip-ups: a bad
#   liveness probe during slow startup causes a restart LOOP (CrashLoopBackOff)
#   even though the app would have become healthy if just given more time —
#   this is exactly what `initialDelaySeconds` is meant to prevent.

---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: default
spec:
  selector:
    app: myapp          # Routes traffic to Pods with this label
  ports:
    - protocol: TCP
      port: 80          # Service port (external)
      targetPort: 3000  # Container port (internal)
  type: ClusterIP       # Internal only. Use LoadBalancer for external access.
```

### ConfigMap & Secret
```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  LOG_LEVEL: "info"
  API_BASE_URL: "https://api.mycompany.com"

---
# k8s/secret.yaml (values must be base64 encoded!)
# echo -n "MyS3cretPass" | base64
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
data:
  db-password: TXlTM2NyZXRQYXNz  # base64 encoded value
  api-key: c29tZWFwaWtleQ==
```

### Ingress (NGINX)
```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
  tls:
    - hosts:
        - myapp.example.com
      secretName: tls-cert-secret
```

---

## Essential kubectl Commands
```bash
# View resources
kubectl get pods -n default
kubectl get services
kubectl get deployments
kubectl get all  # Everything in the namespace

# Describe (shows events at the bottom - great for debugging)
kubectl describe pod myapp-deployment-abc123
kubectl describe service myapp-service

# View logs
kubectl logs myapp-deployment-abc123
kubectl logs myapp-deployment-abc123 -f  # Follow/tail
kubectl logs -l app=myapp --all-containers  # All pods with this label

# Execute into a running pod
kubectl exec -it myapp-deployment-abc123 -- /bin/sh

# Scale a deployment
kubectl scale deployment myapp-deployment --replicas=5

# Apply manifests
kubectl apply -f k8s/          # Apply all YAML files in the k8s/ folder
kubectl delete -f k8s/deployment.yaml

# Rollback
kubectl rollout history deployment/myapp-deployment
kubectl rollout undo deployment/myapp-deployment
kubectl rollout undo deployment/myapp-deployment --to-revision=2
```

---

## AKS Deployment via Azure Pipeline

```yaml
# CD Stage: Deploy to AKS
- stage: Deploy_AKS
  jobs:
    - deployment: DeployToAKS
      environment: 'Production.default'  # Environment.KubernetesNamespace
      pool:
        vmImage: 'ubuntu-latest'
      strategy:
        runOnce:
          deploy:
            steps:
              # Replace BUILD_ID placeholder in YAML with actual build ID
              - bash: |
                  sed -i 's/$(BUILD_ID)/$(Build.BuildId)/g' k8s/deployment.yaml
                displayName: 'Inject Build ID into manifest'

              - task: KubernetesManifest@0
                displayName: 'Create/update K8s Secret for DB password'
                inputs:
                  action: 'createSecret'
                  namespace: 'default'
                  secretType: 'generic'
                  secretName: 'myapp-secrets'
                  secretArguments: '--from-literal=db-password=$(DB_PASSWORD)'
                  kubernetesServiceConnection: 'MyAKS-ServiceConnection'

              - task: KubernetesManifest@0
                displayName: 'Deploy to AKS'
                inputs:
                  action: 'deploy'
                  namespace: 'default'
                  kubernetesServiceConnection: 'MyAKS-ServiceConnection'
                  manifests: |
                    k8s/configmap.yaml
                    k8s/deployment.yaml
                    k8s/service.yaml
                    k8s/ingress.yaml
                  containers: 'mydevopsacr.azurecr.io/myapp:$(Build.BuildId)'
```

---

## Helm Charts (Templated K8s Deployments)

```bash
# Install Helm
brew install helm

# Create a Helm chart
helm create myapp-chart

# Install the chart
helm install myapp-release ./myapp-chart \
  --set image.tag=$(Build.BuildId) \
  --set environment=production \
  --namespace production

# Upgrade an existing release
helm upgrade myapp-release ./myapp-chart \
  --set image.tag=$(Build.BuildId)

# List all releases
helm list -A

# Rollback a release
helm rollback myapp-release 1  # Rollback to revision 1
```

---

## Common Pitfalls & Expert Tips

- **No `resources.requests/limits` set.** Beyond the scheduling/OOM issues noted above, this also breaks Horizontal Pod Autoscaling (HPA scales based on % of *requested* CPU/memory — with no request set, HPA has nothing to calculate a percentage against).
- **Confusing liveness and readiness probes** — a failing readiness probe should mean "temporarily stop sending traffic," not "restart me." Wiring the wrong probe type causes unnecessary restarts (liveness) or zombie Pods still receiving traffic while unhealthy (missing readiness).
- **Secrets stored as plain `Opaque` type with no further protection**, base64 encoded (which is *encoding*, not encryption — anyone with read access to the Secret object can trivially decode it). For real secrets, integrate AKS with Azure Key Vault via the CSI Secrets Store driver instead of raw K8s Secrets.
- **`maxUnavailable: 0` with only 1 replica.** This makes rolling updates impossible (there's no "extra" capacity to shift traffic to, and it can't take the only replica down) — rolling update strategy needs enough replicas to tolerate the configured unavailability.
- **Not setting `namespace` boundaries thoughtfully.** Everything in `default` namespace makes RBAC scoping, resource quotas, and network policies far harder to apply per team/environment.
- **Debugging by re-running `kubectl apply` repeatedly instead of reading `kubectl describe pod` events.** The Events section at the bottom of `describe` almost always names the actual root cause (ImagePullBackOff, insufficient resources, failed probe, etc.) — check it first, every time.

---

## Practical Exercise ✅
1. Create a 2-node AKS cluster using the Azure CLI.
2. Deploy the Docker image you pushed to ACR (Phase 6 exercise) using a `deployment.yaml`.
3. Create a `Service` of type `LoadBalancer` and access the app from your browser using the external IP.
4. Scale the deployment from 1 replica to 3 and watch the pods appear with `kubectl get pods -w`.
5. Simulate a rolling update by pushing a new image tag and re-applying the deployment.

---

## Expert Interview Q&A

**Q: A Pod is stuck in `CrashLoopBackOff`. Walk through your debugging process.**
Start with `kubectl describe pod <name>` and read the Events section — it usually states the direct cause (OOMKilled, failed liveness probe, non-zero exit code). Then `kubectl logs <pod> --previous` to see the crashed container's last output before it died (regular `logs` shows the *current* restarted attempt, which may not have failed yet). Common root causes: an unhandled startup exception, a missing environment variable/config, a liveness probe firing before the app finishes initializing (fix with a higher `initialDelaySeconds` or a startup probe), or the container being OOMKilled because of an undersized memory limit.

**Q: What's the practical difference between a liveness probe and a readiness probe failing?**
A failed liveness probe tells Kubernetes "this container is unresponsive/stuck," triggering a container restart. A failed readiness probe tells Kubernetes "this Pod isn't ready to serve traffic right now," which removes it from the Service's load-balancing endpoints *without* restarting it — used for temporary states like a slow dependency connection or graceful shutdown draining. Using a liveness probe where a readiness probe was intended causes unnecessary restart loops during normal, temporary unavailability.

**Q: Why does Horizontal Pod Autoscaling not work correctly without `resources.requests` defined?**
HPA (when scaling on CPU/memory) computes current utilization as a *percentage of the Pod's requested resources* — no request means there's no baseline to compute a percentage against, so HPA can't make a scaling decision at all (or behaves unpredictably depending on the metric source). Setting accurate `requests` is a prerequisite for resource-based autoscaling to function correctly.

**Q: Why would you use the AKS Key Vault CSI driver instead of native Kubernetes Secrets for sensitive values?**
Native Kubernetes Secrets are only base64-*encoded* (trivially reversible) and, without additional encryption-at-rest configuration on the cluster's etcd, are stored in a way that's easier to expose than a proper secrets manager. The Key Vault CSI driver mounts secrets from Azure Key Vault directly into Pods at runtime (as files or env vars) without ever persisting the raw secret in Kubernetes' own storage — centralizing secret rotation, auditing, and access control in Key Vault instead of duplicating it across cluster manifests.
