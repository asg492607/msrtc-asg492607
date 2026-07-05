# Compliance Operations Guide

## Policy-as-Code
MSRTC uses Kyverno to enforce security policies at the Kubernetes API Server level. 
If a developer attempts to deploy a Pod without `runAsNonRoot: true`, the API server will reject the request outright, preventing the security violation before it ever starts running.

## Evidence Collection
Auditors require proof. Instead of manually taking screenshots, the `generate-evidence.yml` GitHub Action automatically runs on the 1st of every month, dumping the exact state of our IAM policies and Kubernetes RBAC into a zip file.
