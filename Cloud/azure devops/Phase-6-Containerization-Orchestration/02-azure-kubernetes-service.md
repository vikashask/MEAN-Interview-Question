# Azure Kubernetes Service (AKS)

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

## Practical Exercise ✅
1. Create a 2-node AKS cluster using the Azure CLI.
2. Deploy the Docker image you pushed to ACR (Phase 6 exercise) using a `deployment.yaml`.
3. Create a `Service` of type `LoadBalancer` and access the app from your browser using the external IP.
4. Scale the deployment from 1 replica to 3 and watch the pods appear with `kubectl get pods -w`.
5. Simulate a rolling update by pushing a new image tag and re-applying the deployment.
