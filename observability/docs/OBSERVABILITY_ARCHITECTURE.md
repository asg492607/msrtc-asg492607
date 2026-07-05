# Observability Architecture

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
