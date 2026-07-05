# Frontend Integration Guide

Welcome to the MSRTC Backend! This guide provides everything you need to start building the Passenger App and Depot Dashboards.

## 1. SDKs
Stop writing `fetch` calls! We automatically generate strongly-typed SDKs for you:
* **TypeScript (React/Next.js):** `npm install @msrtc/sdk-ts`
* **Kotlin (Android):** Included in the internal Maven repo.
* **Swift (iOS):** Available via Swift Package Manager.

## 2. Authentication
All requests must be routed through the API Gateway at `api.msrtc.gov.in`. 
Include your JWT in the header: `Authorization: Bearer <token>`.

## 3. Environments
* **Development:** `dev-api.msrtc.internal` (Unstable, continuous deployments)
* **Staging:** `staging-api.msrtc.internal` (Stable, matches production data shape)
* **Production:** `api.msrtc.gov.in` (Do not use for local testing!)
