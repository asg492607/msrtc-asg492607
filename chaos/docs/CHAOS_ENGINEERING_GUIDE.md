# Chaos Engineering Guide

## Objective
We intentionally break our Staging environment to prove that our production environment will survive when real infrastructure failures occur.

## The Blast Radius
**NEVER** run these experiments manually in Production. 
All Chaos Engine CRDs are strictly scoped to the `msrtc-staging` namespace.

## Validation Strategy
Chaos is meaningless without Observability. 
1. We run `chaos-pipeline.yml`.
2. The pipeline triggers the `pod-delete` experiment.
3. The pipeline immediately queries the Prometheus API to check the `booking-success-rate` SLO.
4. If the success rate drops below 99.9%, the test FAILS. This means our retries or circuit breakers are misconfigured.
