# API Versioning & Deprecation Policy

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
