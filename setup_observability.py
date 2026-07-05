import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
obs_dir = os.path.join(base_dir, "observability")

dirs = [
    "opentelemetry",
    "prometheus/alerts",
    "grafana/dashboards",
    "jaeger",
    "loki",
    "synthetic",
    "slos",
    "docs"
]

for d in dirs:
    os.makedirs(os.path.join(obs_dir, d), exist_ok=True)

# 1. OpenTelemetry Collector
otel_yaml = """apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-conf
  labels:
    app: opentelemetry
    component: otel-collector-conf
spec:
  data:
    otel-collector-config: |
      receivers:
        otlp:
          protocols:
            grpc:
            http:
      processors:
        batch:
        memory_limiter:
          check_interval: 1s
          limit_mib: 4000
          spike_limit_mib: 800
      exporters:
        prometheus:
          endpoint: "0.0.0.0:8889"
        jaeger:
          endpoint: "jaeger-collector.observability.svc.cluster.local:14250"
          tls:
            insecure: true
        loki:
          endpoint: "http://loki.observability.svc.cluster.local:3100/loki/api/v1/push"
      service:
        pipelines:
          traces:
            receivers: [otlp]
            processors: [memory_limiter, batch]
            exporters: [jaeger]
          metrics:
            receivers: [otlp]
            processors: [memory_limiter, batch]
            exporters: [prometheus]
          logs:
            receivers: [otlp]
            processors: [memory_limiter, batch]
            exporters: [loki]
"""
with open(os.path.join(obs_dir, "opentelemetry/otel-collector-config.yaml"), "w", encoding="utf-8") as f: f.write(otel_yaml)


# 2. Prometheus Alerting Rules
alerts_yaml = """groups:
- name: msrtc.alerts
  rules:
  - alert: HighErrorRate
    expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: High HTTP 5xx error rate detected
      description: "More than 5% of requests are failing in the last 5 minutes."

  - alert: HighLatency
    expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 2.0
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: P95 Latency is over 2 seconds
      description: "API latency is degrading, currently above 2s for 5m."

  - alert: KafkaConsumerLag
    expr: sum by (consumergroup, topic) (kafka_consumergroup_lag) > 1000
    for: 3m
    labels:
      severity: critical
    annotations:
      summary: Kafka consumer lag is too high
      description: "Consumer group {{ $labels.consumergroup }} is lagging behind by over 1000 messages."
"""
with open(os.path.join(obs_dir, "prometheus/alerts/msrtc-alerts.yaml"), "w", encoding="utf-8") as f: f.write(alerts_yaml)


# 3. Synthetic Monitoring (K6)
k6_js = """import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1, // Single virtual user for health checking
  duration: '1m',
};

export default function () {
  // Simulate a user checking routes
  const res = http.get('http://api.msrtc.internal/v1/routes?source=MUM&destination=PUNE');
  check(res, {
    'status was 200': (r) => r.status == 200,
    'transaction time OK': (r) => r.timings.duration < 500,
  });
  sleep(5); // Run every 5 seconds
}
"""
with open(os.path.join(obs_dir, "synthetic/health-journey.js"), "w", encoding="utf-8") as f: f.write(k6_js)


# 4. SLO Definitions
slo_yaml = """apiVersion: slo.custom.io/v1
kind: ServiceLevelObjective
metadata:
  name: booking-success-rate
spec:
  service: booking-service
  description: "99.9% of booking requests must succeed"
  indicator:
    prometheus:
      success: sum(rate(http_requests_total{job="booking-service", status!~"5.."}[30d]))
      total: sum(rate(http_requests_total{job="booking-service"}[30d]))
  objective: 99.9
  window: 30d
"""
with open(os.path.join(obs_dir, "slos/booking-slo.yaml"), "w", encoding="utf-8") as f: f.write(slo_yaml)


# 5. Documentation
docs_arch = """# Observability Architecture

## OpenTelemetry (OTel)
MSRTC uses OpenTelemetry as the vendor-neutral standard for telemetry ingestion.
Instead of sending metrics directly to Prometheus or traces directly to Jaeger, all microservices send OTLP (OpenTelemetry Protocol) data to the `otel-collector`.

## The Pipeline
1. **Instrumented Service** -> sends OTLP data -> **OTel Collector**
2. **OTel Collector** -> routes to:
   * **Prometheus** (Metrics)
   * **Jaeger** (Traces)
   * **Loki** (Logs)
3. **Grafana** -> queries Prometheus, Jaeger, and Loki to render the unified SRE dashboard.
"""
with open(os.path.join(obs_dir, "docs/OBSERVABILITY_ARCHITECTURE.md"), "w", encoding="utf-8") as f: f.write(docs_arch)

docs_runbook = """# Alert Runbook

## HighErrorRate (HTTP 5xx > 5%)
1. Open the Grafana **Service Mesh Dashboard**.
2. Identify the specific microservice throwing 5xx errors.
3. Open Jaeger, filter by that service and `error=true`.
4. Look at the trace span to see if the database or Redis failed.
5. If it's a code regression from a recent deployment, trigger an Argo Rollout rollback.
"""
with open(os.path.join(obs_dir, "docs/ALERT_RUNBOOK.md"), "w", encoding="utf-8") as f: f.write(docs_runbook)

print("Observability Platform Scaffolded")
