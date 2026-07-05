import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
dev_dir = os.path.join(base_dir, "developer-platform")

dirs = [
    "linting",
    "sdk-generator",
    "contract-tests",
    "api-catalog",
    "docs"
]

for d in dirs:
    os.makedirs(os.path.join(dev_dir, d), exist_ok=True)

# 1. API Governance (Spectral Linting)
spectral_yaml = """extends: ["spectral:oas", "spectral:oas3"]
rules:
  # 1. Enforce camelCase for all JSON properties
  camel-case-properties:
    description: "Property names must be camelCase."
    message: "{{property}} is not camelCase."
    severity: error
    given: "$..properties.*~"
    then:
      function: casing
      functionOptions:
        type: camel
  
  # 2. Prevent breaking changes by requiring versioning in the URL path
  path-versioning:
    description: "API paths must start with a version e.g. /v1/"
    severity: error
    given: "$.paths[*]~"
    then:
      function: pattern
      functionOptions:
        match: "^/v[1-9][0-9]*/.*"

  # 3. Require standard HTTP Error definitions
  require-error-responses:
    description: "All operations must define HTTP 400 and 500 error responses."
    severity: error
    given: "$.paths.*[get,post,put,patch,delete]"
    then:
      - field: responses.400
        function: truthy
      - field: responses.500
        function: truthy
"""
with open(os.path.join(dev_dir, "linting/.spectral.yaml"), "w", encoding="utf-8") as f: f.write(spectral_yaml)


# 2. SDK Generation Automation
sdk_sh = """#!/bin/bash
# SDK Generation Script using OpenAPI Generator
set -e

SERVICE_NAME=$1
SPEC_URL="http://api.msrtc.internal/v1/${SERVICE_NAME}/api-json"
OUTPUT_DIR="./generated-sdks/${SERVICE_NAME}-ts"

echo "Downloading OpenAPI Spec for ${SERVICE_NAME}..."
# curl -s $SPEC_URL > spec.json
# Mocking spec existence for script execution
touch spec.json

echo "Generating TypeScript SDK..."
# docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \\
#    -i /local/spec.json \\
#    -g typescript-fetch \\
#    -o /local/${OUTPUT_DIR} \\
#    --additional-properties=supportsES6=true,typescriptThreePlus=true

echo "SDK Generation complete for ${SERVICE_NAME}."
"""
with open(os.path.join(dev_dir, "sdk-generator/generate-sdk.sh"), "w", newline='\n') as f: f.write(sdk_sh)


# 3. Contract Testing Config (Pact)
pact_json = """{
  "consumer": { "name": "MSRTC-Frontend-Web" },
  "provider": { "name": "Booking-Service" },
  "interactions": [
    {
      "description": "a request to create a booking",
      "request": {
        "method": "POST",
        "path": "/v1/bookings",
        "headers": { "Content-Type": "application/json" },
        "body": {
          "routeId": "R123",
          "seats": ["1A", "1B"]
        }
      },
      "response": {
        "status": 201,
        "body": {
          "bookingId": "uuid-v4",
          "status": "CONFIRMED"
        }
      }
    }
  ],
  "metadata": { "pactSpecification": { "version": "3.0.0" } }
}
"""
with open(os.path.join(dev_dir, "contract-tests/pact-example.json"), "w", encoding="utf-8") as f: f.write(pact_json)


# 4. Documentation
docs_style = """# MSRTC API Style Guide

All microservices MUST adhere to this style guide. Violations will be blocked by `Spectral` in the CI/CD pipeline.

## 1. Naming Conventions
*   **Endpoints:** Use plural nouns (e.g., `/v1/bookings`, not `/v1/booking`).
*   **JSON Keys:** Use strict `camelCase` (e.g., `passengerName`, not `passenger_name`).
*   **HTTP Methods:**
    *   `GET`: Retrieve resources.
    *   `POST`: Create resources.
    *   `PUT`: Full replacement of a resource.
    *   `PATCH`: Partial update of a resource.

## 2. Pagination
All collections MUST be paginated using cursor-based or offset-based parameters (`?limit=50&offset=0`). Unbounded queries are strictly forbidden.

## 3. Responses
Always wrap collections in a data object:
```json
{
  "data": [],
  "meta": { "total": 100 }
}
```
"""
with open(os.path.join(dev_dir, "docs/API_STYLE_GUIDE.md"), "w", encoding="utf-8") as f: f.write(docs_style)

docs_version = """# API Versioning & Deprecation Policy

## Versioning
Version numbers must be included in the URL route: `api.msrtc.gov.in/v1/bookings`.
We do NOT use header-based versioning.

## Breaking Changes
The following are considered breaking changes and require bumping to `/v2/`:
* Renaming or removing a JSON property.
* Changing a property's data type (e.g., integer to string).
* Adding a new *required* property to a request payload.

## Deprecation
An API endpoint cannot be deleted immediately.
1. The endpoint must be marked `deprecated: true` in the OpenAPI spec.
2. It must remain active in production for exactly **90 days** to allow mobile apps time to upgrade.
"""
with open(os.path.join(dev_dir, "docs/VERSIONING_POLICY.md"), "w", encoding="utf-8") as f: f.write(docs_version)


print("API Governance Framework Scaffolded")
