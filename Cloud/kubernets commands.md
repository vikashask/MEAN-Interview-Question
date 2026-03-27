# Kubernetes Commands

This document contains a comprehensive collection of useful Kubernetes commands categorized for easy reference.

---

## Cluster Info

Get basic information about the cluster:

```bash
kubectl cluster-info
kubectl version
kubectl get componentstatuses
kubectl get nodes
```

---

## Nodes & Pods

### Nodes

List all nodes in the cluster:

```bash
kubectl get nodes
kubectl describe node <node-name>
```

### Pods

List all pods in all namespaces:

```bash
kubectl get pods --all-namespaces
```

List pods in the current namespace:

```bash
kubectl get pods
kubectl get pods -o wide
kubectl describe pod <pod-name>
```

Delete a pod:

```bash
kubectl delete pod <pod-name>
```

Execute a command inside a running pod:

```bash
kubectl exec -it <pod-name> -- /bin/bash
# or for a single command
kubectl exec <pod-name> -- <command>
```

Port-forward a local port to a pod:

```bash
kubectl port-forward pod/<pod-name> <local-port>:<pod-port>
```

---

## Deployments & Services

### Deployments

List deployments:

```bash
kubectl get deployments
kubectl describe deployment <deployment-name>
```

Create a deployment:

```bash
kubectl create deployment <deployment-name> --image=<image-name>
```

Update a deployment image:

```bash
kubectl set image deployment/<deployment-name> <container-name>=<new-image>
```

Rollout status and history:

```bash
kubectl rollout status deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name>
kubectl rollout undo deployment/<deployment-name>
```

Scale a deployment:

```bash
kubectl scale deployment/<deployment-name> --replicas=<number>
```

Delete a deployment:

```bash
kubectl delete deployment <deployment-name>
```

### Services

List services:

```bash
kubectl get services
kubectl describe service <service-name>
```

Expose a deployment as a service:

```bash
kubectl expose deployment <deployment-name> --type=<ClusterIP|NodePort|LoadBalancer> --port=<port> --target-port=<target-port>
```

Delete a service:

```bash
kubectl delete service <service-name>
```

---

## ConfigMaps & Secrets

### ConfigMaps

Create a ConfigMap from a file:

```bash
kubectl create configmap <configmap-name> --from-file=<file-path>
```

Create a ConfigMap from literal values:

```bash
kubectl create configmap <configmap-name> --from-literal=key1=value1 --from-literal=key2=value2
```

Get ConfigMaps:

```bash
kubectl get configmaps
kubectl describe configmap <configmap-name>
```

### Secrets

Create a secret from literal values:

```bash
kubectl create secret generic <secret-name> --from-literal=username=admin --from-literal=password='S!B\*d$zDsb='
```

Create a secret from a file:

```bash
kubectl create secret generic <secret-name> --from-file=<file-path>
```

Get secrets:

```bash
kubectl get secrets
kubectl describe secret <secret-name>
```

---

## Logs & Debugging

Get logs from a pod:

```bash
kubectl logs <pod-name>
kubectl logs -f <pod-name>               # Follow logs
kubectl logs <pod-name> -c <container>  # Logs from a specific container
```

Debug a pod by running a temporary pod with the same image:

```bash
kubectl run -i --tty debug --image=<image-name> --restart=Never -- /bin/bash
```

Check events in the cluster:

```bash
kubectl get events --sort-by='.metadata.creationTimestamp'
```

---

## Namespaces

List namespaces:

```bash
kubectl get namespaces
```

Create a namespace:

```bash
kubectl create namespace <namespace-name>
```

Delete a namespace:

```bash
kubectl delete namespace <namespace-name>
```

Use a specific namespace for commands:

```bash
kubectl config set-context --current --namespace=<namespace-name>
kubectl get pods -n <namespace-name>
```

---

## Scaling & Autoscaling

Scale a deployment manually:

```bash
kubectl scale deployment/<deployment-name> --replicas=<number>
```

Autoscale a deployment:

```bash
kubectl autoscale deployment <deployment-name> --min=<min-replicas> --max=<max-replicas> --cpu-percent=<target-cpu-utilization>
```

Check autoscaler status:

```bash
kubectl get hpa
kubectl describe hpa <hpa-name>
```

---

## Context & Config

View current context:

```bash
kubectl config current-context
```

List all contexts:

```bash
kubectl config get-contexts
```

Switch context:

```bash
kubectl config use-context <context-name>
```

View config info:

```bash
kubectl config view
```

---

## Cleanup

Delete all pods in a namespace:

```bash
kubectl delete pods --all
```

Delete all resources in a namespace:

```bash
kubectl delete all --all
```

Delete pods by label:

```bash
kubectl delete pods -l <label-selector>
```

---

## Most Frequently Asked in Interviews

- **kubectl get pods** — List pods and understand pod status.
- **kubectl describe pod <pod-name>** — Get detailed info about a pod.
- **kubectl logs <pod-name>** — View logs to troubleshoot.
- **kubectl exec -it <pod-name> -- /bin/bash** — Access pod shell for debugging.
- **kubectl apply -f <file.yaml>** — Apply configuration changes.
- **kubectl rollout status deployment/<deployment-name>** — Check deployment rollout status.
- **kubectl scale deployment/<deployment-name> --replicas=<number>** — Scale applications.
- **kubectl get nodes** and **kubectl describe node <node-name>** — Check node status and resources.
- **kubectl get services** — Understand service types and networking.
- **kubectl config use-context** — Manage multiple clusters and contexts.
- Understanding **Pods, Deployments, Services, ConfigMaps, Secrets, Namespaces, and Autoscaling** concepts.

---

This cheat sheet should help you quickly access and use the most important Kubernetes commands for cluster management, debugging, and deployment tasks.
