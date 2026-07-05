import os
import yaml

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"

# Directory structure
dirs = [
    "security/policies",
    "security/docs",
    ".github/workflows"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)


# 1. GitHub Actions Pipeline (security-pipeline.yml)
pipeline_yaml = """name: DevSecOps Supply Chain Security Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  secret-scan:
    name: Secret Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - name: TruffleHog OSS
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  sast-scan:
    name: SAST (Static Analysis)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: "p/default"

  iac-scan:
    name: Infrastructure as Code Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Checkov GitHub Action
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/

  container-security:
    name: Container Scan & SBOM
    runs-on: ubuntu-latest
    needs: [secret-scan, sast-scan, iac-scan]
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker Image (Mock)
        run: echo "Building container..."
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'ghcr.io/msrtc/api-gateway:latest'
          format: 'table'
          exit-code: '1'
          ignore-unfixed: true
          vuln-type: 'os,library'
          severity: 'CRITICAL,HIGH'
      - name: Generate SBOM (Syft)
        uses: anchore/sbom-action@v0
        with:
          image: ghcr.io/msrtc/api-gateway:latest
          artifact-name: sbom-api-gateway.spdx.json
"""
with open(os.path.join(base_dir, ".github/workflows/security-pipeline.yml"), "w", encoding="utf-8") as f: f.write(pipeline_yaml)


# 2. Kubernetes Admission Policy (Kyverno)
k8s_policy = """apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: enforce-pod-security
  annotations:
    policies.kyverno.io/title: Enforce Pod Security Standards
    policies.kyverno.io/description: >-
      Ensures that all MSRTC containers run securely, forbidding root escalation
      and requiring read-only root filesystems where possible.
spec:
  validationFailureAction: enforce
  rules:
    - name: restrict-escalation
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Privilege escalation is forbidden."
        pattern:
          spec:
            containers:
              - securityContext:
                  allowPrivilegeEscalation: false
    - name: require-run-as-non-root
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Containers must run as a non-root user."
        pattern:
          spec:
            containers:
              - securityContext:
                  runAsNonRoot: true
"""
with open(os.path.join(base_dir, "security/policies/k8s-admission.yaml"), "w", encoding="utf-8") as f: f.write(k8s_policy)


# 3. Secure Development Guide
dev_guide = """# Secure Development Guide

## 1. Credentials & Secrets
* **NEVER** hardcode AWS Keys, Database Passwords, or JWT Secrets in the source code.
* Use environment variables mapped via Terraform/Kubernetes ConfigMaps.
* Our CI/CD pipeline runs `TruffleHog`; any committed secret will instantly fail the build.

## 2. Dependency Management
* Run `npm audit` locally before committing.
* Do not use outdated packages. `Snyk` checks run on every PR.
* Only pull Docker base images from official verified publishers.

## 3. Data Validation
* Always use `@nestjs/class-validator` DTOs.
* Never trust incoming JSON structures without validation to prevent NoSQL/SQL injection attacks.
"""
with open(os.path.join(base_dir, "security/docs/SECURE_DEVELOPMENT_GUIDE.md"), "w", encoding="utf-8") as f: f.write(dev_guide)


# 4. Vulnerability Response Runbook
vuln_runbook = """# Vulnerability Response Runbook

## Objective
Standard Operating Procedure (SOP) when a CRITICAL or HIGH CVE (Common Vulnerabilities and Exposures) is detected in production.

## Workflow
1. **Triage:** Review the CVE scan from `Trivy` or `Snyk` on the GitHub Security Dashboard.
2. **Assess Impact:** Determine if the vulnerable library is actually executed by our codebase (e.g. a vulnerability in a test package vs. an active web server component).
3. **Patch:** 
   * Update the package version in `package.json`.
   * Update the Docker base image in the `Dockerfile`.
4. **Deploy:** Merge the fix to `main`. ArgoCD will auto-sync the patched container to production.
5. **Post-Mortem:** Document the incident in the `security/docs/incidents/` log.
"""
with open(os.path.join(base_dir, "security/docs/VULNERABILITY_RESPONSE_RUNBOOK.md"), "w", encoding="utf-8") as f: f.write(vuln_runbook)


print("DevSecOps Supply Chain Platform scaffolded successfully.")
