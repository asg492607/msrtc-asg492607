import os
import yaml

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
helm_dir = os.path.join(base_dir, "helm/msrtc-service")
helm_templates = os.path.join(helm_dir, "templates")
k8s_dir = os.path.join(base_dir, "k8s")
argocd_dir = os.path.join(k8s_dir, "argocd")

os.makedirs(helm_templates, exist_ok=True)
os.makedirs(argocd_dir, exist_ok=True)

# 1. Helm Chart Metadata
chart_yaml = """apiVersion: v2
name: msrtc-service
description: A universal Helm chart for MSRTC Microservices
type: application
version: 1.0.0
appVersion: "1.0.0"
"""
with open(os.path.join(helm_dir, "Chart.yaml"), "w", encoding="utf-8") as f: f.write(chart_yaml)

values_yaml = """# Default values for msrtc-service.
replicaCount: 2

image:
  repository: ghcr.io/asg492607/msrtc-service
  pullPolicy: IfNotPresent
  tag: "latest"

service:
  type: ClusterIP
  port: 3000

ingress:
  enabled: false
  className: "nginx"
  annotations: {}
  hosts:
    - host: api.msrtc.internal
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

env: {}
"""
with open(os.path.join(helm_dir, "values.yaml"), "w", encoding="utf-8") as f: f.write(values_yaml)


# 2. Helm Templates
deploy_tmpl = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "msrtc-service.fullname" . }}
  labels:
    app: {{ include "msrtc-service.name" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ include "msrtc-service.name" . }}
  template:
    metadata:
      labels:
        app: {{ include "msrtc-service.name" . }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          env:
            {{- range $key, $val := .Values.env }}
            - name: {{ $key }}
              value: {{ $val | quote }}
            {{- end }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
"""
with open(os.path.join(helm_templates, "deployment.yaml"), "w", encoding="utf-8") as f: f.write(deploy_tmpl)

svc_tmpl = """apiVersion: v1
kind: Service
metadata:
  name: {{ include "msrtc-service.fullname" . }}
  labels:
    app: {{ include "msrtc-service.name" . }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app: {{ include "msrtc-service.name" . }}
"""
with open(os.path.join(helm_templates, "service.yaml"), "w", encoding="utf-8") as f: f.write(svc_tmpl)

hpa_tmpl = """{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "msrtc-service.fullname" . }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "msrtc-service.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    {{- end }}
{{- end }}
"""
with open(os.path.join(helm_templates, "hpa.yaml"), "w", encoding="utf-8") as f: f.write(hpa_tmpl)

helper_tmpl = """{{/* Expand the name of the chart. */}}
{{- define "msrtc-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Create a default fully qualified app name. */}}
{{- define "msrtc-service.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
"""
with open(os.path.join(helm_templates, "_helpers.tpl"), "w", encoding="utf-8") as f: f.write(helper_tmpl)


# 3. ArgoCD App
argo_app = """apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: msrtc-production
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/asg492607/msrtc-asg492607.git'
    targetRevision: HEAD
    path: helm/environments/production
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: msrtc-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
"""
with open(os.path.join(argocd_dir, "production-app.yaml"), "w", encoding="utf-8") as f: f.write(argo_app)


# 4. GitOps Workflow Documentation
gitops_doc = """# GitOps Workflow (ArgoCD)

## Overview
The MSRTC platform is deployed using a strict GitOps model. No engineer should ever run `kubectl apply` or `helm upgrade` against the production cluster. Instead, ArgoCD monitors this GitHub repository and automatically synchronizes the cluster state.

## How to Deploy a New Service
1. The CI pipeline builds the Docker image and tags it with the Git commit SHA (e.g., `ghcr.io/msrtc/booking-service:abc1234`).
2. The CI pipeline automatically updates the `helm/environments/production/values-booking-service.yaml` file with the new image tag and commits it back to GitHub.
3. ArgoCD detects the commit on the `main` branch.
4. ArgoCD triggers a rolling deployment in the Kubernetes cluster.

## Universal Helm Chart
Instead of 20 different sets of YAML files, we use the universal `helm/msrtc-service` chart.
To configure a specific microservice, you simply provide a `values-<service-name>.yaml` file that overrides the defaults.

Example `values-api-gateway.yaml`:
```yaml
replicaCount: 3
image:
  repository: ghcr.io/msrtc/api-gateway
ingress:
  enabled: true
  hosts:
    - host: api.msrtc.gov.in
```
"""
with open(os.path.join(base_dir, "k8s/GITOPS_WORKFLOW.md"), "w", encoding="utf-8") as f: f.write(gitops_doc)

print("Kubernetes GitOps Platform scaffolded successfully.")
