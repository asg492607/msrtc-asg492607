# API Contract Freeze (v1.0)

## Declaration
As of this release, all OpenAPI specifications under the `/v1/` namespace are officially **FROZEN**.

## Policy for Backend Developers
1. **No Breaking Changes:** You may NOT rename fields, change data types, or add *required* fields to any existing endpoint.
2. **Backward Compatibility:** You may safely add *optional* fields to responses.
3. **Major Changes:** Any breaking change must be introduced via a new `/v2/` endpoint, and the `/v1/` endpoint must enter the 90-day deprecation cycle.

This ensures our frontend and mobile teams can build against a stable foundation.
