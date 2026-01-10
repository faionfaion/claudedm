---
name: kubectl-access
description: Use when working with Kubernetes clusters (EKS). Shows available clusters, contexts, and common kubectl commands for FinRay platform.
---

# kubectl-access

Use this skill when working with Kubernetes clusters for the FinRay platform.

## Available EKS Clusters

All clusters are in **us-east-1** region.

| Cluster | Context Name | Purpose |
|---------|--------------|---------|
| shared2-cluster-finray | shared2-cluster-finray | Shared development/staging environment |
| clients-cluster-finray | clients-cluster-finray | Client-facing production |
| performance-cluster-finray | performance-cluster-finray | Performance testing |

## Accessing Clusters

### Switch Context

```bash
# List all contexts
kubectl config get-contexts

# Switch to a specific cluster
kubectl config use-context shared2-cluster-finray
kubectl config use-context clients-cluster-finray
kubectl config use-context performance-cluster-finray
```

### Run Commands on Specific Cluster

Use `--context` flag to run commands without switching:

```bash
kubectl --context=shared2-cluster-finray get pods
kubectl --context=clients-cluster-finray get deployments
kubectl --context=performance-cluster-finray get services
```

## Common Commands

### View Resources

```bash
# Get nodes
kubectl --context=shared2-cluster-finray get nodes

# Get all pods in all namespaces
kubectl --context=shared2-cluster-finray get pods -A

# Get pods in specific namespace
kubectl --context=shared2-cluster-finray get pods -n finray

# Get deployments
kubectl --context=shared2-cluster-finray get deployments -n finray

# Get services
kubectl --context=shared2-cluster-finray get services -n finray
```

### View Logs

```bash
# Get logs from a pod
kubectl --context=shared2-cluster-finray logs <pod-name> -n finray

# Follow logs
kubectl --context=shared2-cluster-finray logs -f <pod-name> -n finray

# Get logs from specific container
kubectl --context=shared2-cluster-finray logs <pod-name> -c <container-name> -n finray
```

### Debugging

```bash
# Describe a pod
kubectl --context=shared2-cluster-finray describe pod <pod-name> -n finray

# Execute command in pod
kubectl --context=shared2-cluster-finray exec -it <pod-name> -n finray -- /bin/bash

# Port forward
kubectl --context=shared2-cluster-finray port-forward <pod-name> 8080:8080 -n finray
```

## Cluster Details

### shared2-cluster-finray (Default)
- **Server:** https://93299036D6226274B50A5D31905661A3.gr7.us-east-1.eks.amazonaws.com
- **Nodes:** 4
- **K8s Version:** v1.33.5

### clients-cluster-finray
- **Server:** https://62C39CA6B779380243E883C32E161415.gr7.us-east-1.eks.amazonaws.com
- **Nodes:** 2
- **K8s Version:** v1.33.5

### performance-cluster-finray
- **Server:** https://3729838149E79FC30BD855A3D18D67A6.gr7.us-east-1.eks.amazonaws.com
- **Nodes:** 2
- **K8s Version:** v1.33.5

## Authentication

Authentication is handled via `aws-iam-authenticator` configured in `~/.kube/config`. The user `ruslanm` has kubectl access but limited AWS API permissions (no `eks:ListClusters`).

## Notes

- Always specify `--context` to avoid running commands on wrong cluster
- Default namespace for FinRay workloads is typically `finray`
- Use `-n` or `--namespace` flag to specify namespace
