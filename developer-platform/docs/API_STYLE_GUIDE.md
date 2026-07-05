# MSRTC API Style Guide

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
